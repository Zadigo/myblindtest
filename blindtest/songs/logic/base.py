import asyncio
import dataclasses
import json
import os
import pathlib
import random
from collections import defaultdict
from functools import cached_property, lru_cache
from typing import List, Optional, Union

from asgiref.sync import async_to_sync
# import firebase_admin
# from firebase_admin import firestore, credentials
from channels.db import database_sync_to_async
from django.conf import settings
from django.core import exceptions
from django.core.cache import cache
from django.db import models
from django.utils.crypto import get_random_string
from songs.api import serializers
from songs.models import Song
from songs.processors import FuzzyMatcher
from songs.song_typings import DictAny


@dataclasses.dataclass
class Player:
    id: str = None
    position: int = 0
    name: str = None
    color: str = None
    points: int = 0
    team: Optional[str] = None
    correctAnswers: List[int] = dataclasses.field(default_factory=list)
    speciality: Optional[str] = None

    def __hash__(self):
        return hash((self.name, self.id, self.position))

    def __eq__(self, value: Union[str, 'Player']):
        if isinstance(value, str):
            return any([
                self.name == value,
                self.id == value,
                str(self.position) == value
            ])

        return any([
            self.name == value.name,
            self.id == value.id,
            self.position == value.position
        ])


class BaseGameLogicMixin:
    """Base game logic mixin containing shared logic between
    individual and team-based blindtests."""

    difficulties = ['All', 'Easy', 'Medium', 'Semi-Pro', 'Difficult', 'Expert']
    game_duration: int = 30
    cache_timeout: int = 3600

    @property
    def players(self) -> list[Player]:
        return list(self._players.values())

    @property
    def player_values(self) -> dict[str, dict[str, str | int]]:
        return {key: dataclasses.asdict(player) for key, player in self._players.items()}

    @property
    def load_json_genres(self) -> dict[str, List[str]]:
        genres = cache.get('all_genres', None)
        if genres is not None:
            return genres

        path = settings.MEDIA_PATH / 'genres.json'
        with open(path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
            cache.set('all_genres', data, self.cache_timeout + 3600)
            return data

    @cached_property
    def genres_categories(self) -> list[str]:
        return list(self.load_json_genres.keys())

    @database_sync_to_async
    def get_songs(self, temporary_genre: Optional[str] = None, exclude: List[int] = []) -> List[int]:
        cache_key = f'songs_{self.difficulty}_{self.genre}'
        cached_songs = cache.get(cache_key)

        if cached_songs is not None:
            song_ids = [
                song_id for song_id in cached_songs
                if song_id not in exclude
            ]
            random.shuffle(song_ids)
            return song_ids

        qs = Song.objects.all()

        if self.difficulty != 'All':
            value = self.difficulties.index(self.difficulty)
            qs = qs.filter(difficulty__gte=value)

        if self.genre != 'All':
            qs = qs.filter(genre__icontains=self.genre)

        if exclude:
            qs = qs.exclude(id__in=exclude)

        if temporary_genre is not None:
            if self.genre == 'All':
                qs = qs.exclude(genre=temporary_genre)
            self.send_error(
                'The current blindtest is not set to contain all genres', error='warning')

        song_ids = list(qs.values_list('id', flat=True))
        random.shuffle(song_ids)
        cache.set(cache_key, song_ids, self.cache_timeout)

        return song_ids

    @database_sync_to_async
    def get_song(self, song_id: int) -> dict[str, Union[str, int]]:
        """Returns a serialized song by its ID"""
        try:
            song = Song.objects.get(id=song_id)
        except exceptions.ObjectDoesNotExist:
            raise
        else:
            serializer = serializers.SongSerializer(instance=song)
            return serializer.data

    @database_sync_to_async
    def queryset(self, selected_ids, current_song_id) -> list[dict[str, Union[str, int]]]:
        qs = Song.objects.filter(id__in=selected_ids)
        logic = models.When(models.Q(id=current_song_id), then=True)
        case = models.Case(
            logic,
            default=False,
            output_field=models.BooleanField()
        )
        qs = qs.annotate(is_correct_answer=case)

        fields = ['id', 'name', 'artist__name', 'is_correct_answer']
        picks = list(qs.values(*fields))

        random.shuffle(picks)
        return picks

    @lru_cache(maxsize=128)
    async def random_choice_answers(self, current_song_id: int) -> list[dict[str, Union[str, int]]]:
        """Returns a list of 4 songs including the current song ID"""
        songs = await self.get_songs(exclude=[current_song_id])

        selected_ids = random.sample(songs or [], k=self.number_of_choices)
        selected_ids.append(current_song_id)

        choices = await self.queryset(selected_ids, current_song_id)
        self.current_choice_answers = choices
        return choices

    async def next_song(self, temporary_genre: Optional[str] = None):
        """Returns a song using IDs present in the datbase.

        Or, returns a song within the genre that is passed within
        this function. If the queryset is empty, return a selection
        of all the songs"""
        return await self.get_songs(temporary_genre=temporary_genre, exclude=list(self.played_songs))

    async def calculate_points(self, title_match: bool, artist_match: bool):
        """Calculate points based on match type (title/artist) for
        the player that made the guess"""
        base_points = 0

        # Use the song's difficulty level
        # for the total score
        def factor(value: int):
            if self.difficulty_bonus:
                factor = int(self.current_song['difficulty'])
                return self.point_value * factor
            return value

        if title_match:
            base_points += factor(self.point_value)

        if artist_match:
            base_points += factor(self.point_value)

        return base_points

    async def calculate_multiple_choice_points(self):
        """Calculates points for multiple choice answers"""
        for item in self.player_choices:
            player = self._players.get(item['player_id'], None)

            if player is not None:
                index = item['answer_index']

                try:
                    answer = self.current_choice_answers[index]
                except IndexError:
                    await self.send_error('Invalid answer index submitted')
                    continue
                else:
                    if answer.get('is_correct_answer', False):
                        points = await self.calculate_points(True, False)
                        player.points += points

    async def calculate_loosers_loses_points(self, winner_id: str, title_match: bool = False, artist_match: bool = False):
        """Calculates the points for the winner and then
        deducts points from the losers"""
        winners_points = await self.calculate_points(title_match, artist_match)

        for player in self._players.values():
            if player.id == winner_id:
                player.points += winners_points
                continue

            # Deduct points from losers
            player.points = max(0, player.points - 2)

    async def handle_guess(self, player_id: str, title_match: bool, artist_match: bool):
        """Proxy method that handle the guess for either player by calculating
        points and returning a message dictionary for the frontend. This should be
        implemented in subclasses."""
        raise NotImplementedError


@dataclasses.dataclass
class GameSettings():
    """Encapsulates the game settings
    for the current bindtest. This is
    voluntary duplicate of the firebase
    structure from the frontend"""

    difficulty = 'All'
    genre = 'All'

    numberOfRounds = None

    pointValue: int = 1
    difficultyBonus = False
    timeBonus = False

    # fuzzy_matcher = FuzzyMatcher()

    connectionToken = None    

    soloMode = False
    adminPlays = False
    timeLimit = None
    timeRange: List[int] = []

    multipleChoiceAnswers: bool = False
    numberOfChoices: int = 4
    currentChoiceAnswers: List[dict[str, Union[str, int]]] = []
    playerChoices: list[dict[str, Union[str, int]]] = []

    def config_from_dict(self, config: dict) -> list[str]:
        """Configures the game settings from a dictionary."""
        skipped_keys = []

        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
                continue
            skipped_keys.append(key)
        return skipped_keys


@dataclasses.dataclass
class GameState():
    """Initiates the game state for 
    the current blindtest"""

    is_started: bool = False
    current_round: int = 0
    current_song: Optional[dict[str, Union[str, int]]] = None
    played_songs: set[int] = dataclasses.field(default_factory=set)
    paused: bool = False

    _players: defaultdict[str, Player] = defaultdict(Player)
    playerCount: int = 0

    def increase_round(self) -> None:
        self.current_round += 1

    def add_played_song(self, song_id: int) -> None:
        self.played_songs.add(song_id)

    @property
    def players(self) -> list[Player]:
        """Returns a list of player dataclasses"""
        return list(self._players.values())
    
    @property
    def current_song_id(self) -> Optional[int]:
        """Returns the current song ID if available"""
        if self.current_song is not None:
            return self.current_song.get('id', None)
        return None

    @property
    def player_values(self) -> dict[str, dict[str, str | int]]:
        """Returns a dictionary representation of players"""
        return {key: dataclasses.asdict(player) for key, player in self._players.items()}

    def add_player(self, data: dict[str, DictAny]):
        """Adds a player to the current game settings"""
        player_id = data.get('id')
        if player_id is None:
            return False

        if player_id not in self._players:
            self.player_count += 1
            data['position'] = self.player_count
            player = Player(**data)
            self._players[player_id] = player

    



class GameLogicMixin(BaseGameLogicMixin):
    """Game logic for individual players"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_name = 'admin_individual'
        self.device_id = 'admin_individual'



        # self.difficulty = 'All'
        # self.genre = 'All'

        # self.current_round = 0
        # self.number_of_rounds = None

        # self.point_value: int = 1
        # self.difficulty_bonus = False
        # self.time_bonus = False

        # self.is_started = False
        # self.current_song: Optional[dict[str, Union[str, int]]] = None

        # self.played_songs: set[int] = set()
        # self.fuzzy_matcher = FuzzyMatcher()


        # self.connection_token = None

        # # Pin code for the game
        # self.pin_code = random.randint(1000, 9999)
        # self.pending_devices: List[str] = []

        # self.solo_mode = False
        # self.admin_plays = False
        # self.time_limit = None
        # self.time_range: List[int] = []

        # self._players: defaultdict[str, Player] = defaultdict(Player)
        # self.player_count: int = 0

        # self.paused: bool = False

        # # Spcial case where the admin allows the players
        # # to answer using multiple choice answers
        # self.multiple_choice_answers: bool = False
        # self.number_of_choices: int = 4
        # self.current_choice_answers: List[dict[str, Union[str, int]]] = []
        # self.player_choices: list[dict[str, Union[str, int]]] = []

        # Initialize Firebase
        # cert = credentials.Certificate(
        #     os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

        # try:
        #     firebase_admin.initialize_app(cert)
        #     self.firebase_db = firestore.client()
        # except Exception as e:
        #     print('Firebase initialization error:', e)
        #     self.firebase_db = None

        # doc = self.firebase_collection.document('')
        # snapshop = doc.get()
        # doc.update({'active': True})
        # doc.create({'active': True})
        # if snapshop.exists:
        #     snapshop.to_dict()

        self.pin_code = random.randint(1000, 9999)
        self.pending_devices: List[str] = []

        self.game_settings = GameSettings()
        self.game_state = GameState()

    async def handle_guess(self, player_id: str, title_match, artist_match):
        if not self.game_state.current_song:
            return None

        message = {
            'action': None,
            'player_id': player_id,
            'points': 0
        }

        player: Player = self.game_state._players[player_id]

        if title_match or artist_match:
            result = await self.calculate_points(title_match, artist_match)

            message['action'] = 'guess_correct'
            player.points += result
            message['points'] = player.points
            player.correctAnswers.append(self.game_state.current_song_id)
        else:
            message['action'] = 'guess_incorrect'
            message['points'] = player.points

        message['song'] = self.game_state.current_song
        return message

    async def next_song(self, temporary_genre: str = None):
        song_ids = await self.get_songs(
            temporary_genre=temporary_genre,
            exclude=list(self.played_songs)
        )

        if not song_ids:
            await self.send_json({
                'action': 'game_complete',
                'message': 'No songs left',
                'final_scores': self.player_values,
                'songs_played': len(self.played_songs)
            })
            self.is_started = False
            return

        random_id = random.choice(song_ids)
        self.current_song = await self.get_song(random_id)
        self.played_songs.add(random_id)

        await self.send_json({'action': 'song_new', 'song': self.current_song})

        self.current_round += 1

        if self.number_of_rounds is not None:
            if self.current_round > self.number_of_rounds:
                await self.send_json({
                    'action': 'game_complete',
                    'message': 'Final round complete',
                    'final_scores': self.player_values,
                    'songs_played': len(self.played_songs)
                })
                self.is_started = False
                return

        print(self.current_choice_answers)

        if self.multiple_choice_answers:
            message = {
                'action': 'update_possibilities',
                'choices': []
            }

            picks = await self.random_choice_answers(self.current_song['id'])
            message['choices'] = picks

            await self.send_json(message)

            # self.channel_layer.group_send(self.indexed_diffusion_group_name, {
            #     'type': 'game.updates',
            #     'message': message
            # })
