import asyncio
import dataclasses
import random
from typing import List, Optional, Union

from channels.db import database_sync_to_async
from django.core import exceptions
from django.core.cache import cache
from django.utils.crypto import get_random_string
from songs.api import serializers
from songs.models import Song
from songs.processors import FuzzyMatcher
from songs.game_logic.statistics import GameGlobalStatisticsMixin


@dataclasses.dataclass
class Team:
    team_id: str
    name: Optional[str] = None
    color: Optional[str] = None
    points: Optional[int] = 0
    correct_answers: List[int] = dataclasses.field(default_factory=list)
    answer_times: List[int] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash((self.team_id))

    def __eq__(self, value: str):
        return self.team_id == value


class GameLogicMixin(GameGlobalStatisticsMixin):
    difficulties = ['All', 'Easy', 'Medium', 'Semi-Pro', 'Difficult', 'Expert']
    game_duration: int = 30
    cache_timeout: int = 3600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.difficulty = 'All'
        self.genre = 'All'

        # self.start_time = None
        self.current_round = 0
        self.number_of_rounds = None

        self.point_value: int = 1
        self.difficulty_bonus = False
        self.time_bonus = False

        # team_one_id = f'team_{get_random_string(length=12)}'
        # team_two_id = f'team_{get_random_string(length=12)}'
        self.team_one = Team('fake_id_1')
        self.team_two = Team('fake_id_2')

        self.is_started = False
        self.current_song: Optional[dict[str, Union[str, int]]] = None
        self.timer_task: Optional[asyncio.Task] = None

        # Solo mode is a mode where the
        # user tries to guess the songs
        # himself
        self.solo_mode = False
        # Mode where the admin is also
        # part of a team and therefore
        # needs the song information
        # to be deactivated
        self.admin_plays = False

        self.played_songs: set[int] = set()
        self.fuzzy_matcher = FuzzyMatcher()

        self.device_name = 'blind_test'
        self.device_id = f'blind_test_{get_random_string(length=12)}'
        self.connection_token = None
        # Pin code for the game
        self.pin_code = random.randint(1000, 9999)
        self.pending_devices: List[str] = []

    @database_sync_to_async
    def get_songs(self, temporary_genre: Optional[str] = None, exclude: List[int] = []) -> List[int]:
        cache_key = f'songs_{self.difficulty}_{self.genre}'
        cached_songs = cache.get(cache_key)

        if cached_songs is not None:
            return [song_id for song_id in cached_songs if song_id not in exclude]

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
    def get_song(self, song_id: int):
        try:
            song = Song.objects.get(id=song_id)
            serializer = serializers.SongSerializer(instance=song)
            return serializer.data
        except exceptions.ObjectDoesNotExist:
            raise

    async def next_song(self, temporary_genre: str = None):
        """Returns a song using IDs present in the datbase.

        Or, returns a song within the genre that is passed within
        this function. If the queryset is empty, return a selection
        of all the songs"""
        song_ids = await self.get_songs(
            temporary_genre=temporary_genre,
            exclude=list(self.played_songs)
        )

        if not song_ids:
            await self.send_json({
                'action': 'game_complete',
                'message': 'No songs left',
                'final_scores': {
                    'team1': self.team_one_score,
                    'team2': self.team_two_score
                },
                'songs_played': len(self.played_songs)
            })
            self.is_started = False
            return

        random_id = random.choice(song_ids)
        self.current_song = await self.get_song(random_id)
        self.played_songs.add(random_id)

        if self.solo_mode:
            # In solo mode return only the audio
            # of the song not its information since
            # we get those when the user guesses the
            # the song
            await self.send_json({
                'action': 'song_new',
                'song': {
                    'audio_url': self.current_song['audio_url']
                }
            })
        else:
            await self.send_json({
                'action': 'song_new',
                'song': self.current_song
            })

        self.current_round += 1

        if self.number_of_rounds is not None:
            if self.current_round > self.number_of_rounds:
                await self.send_json({
                    'action': 'game_complete',
                    'message': 'Final round complete',
                    'final_scores': {
                        'team1': self.team_one.score,
                        'team2': self.team_two.score
                    },
                    'songs_played': len(self.played_songs)
                })
                self.is_started = False
                return

        # if self.timer_task:
        #     self.timer_task.cancel()
        # self.timer_task = asyncio.create_task(self.timer())

    async def calculate_points(self, title_match: bool, artist_match: bool):
        """Calculate points based on match type and remaining time"""
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

        # Time bonus: more points for quicker answers
        if self.time_bonus:
            # time_multiplier = self.timer_task._coro.cr_frame.f_locals['remaining_time'] / self.game_duration
            coro = self.timer_task.get_coro()
            time_multiplier = (
                coro.cr_frame.f_locals['remaining_time'] /
                self.game_duration
            )
            return int(base_points + (1 + time_multiplier))

        return base_points

    async def timer(self):
        remaining_time = self.game_duration
        try:
            while remaining_time > 0 and self.is_started:
                await self.send_json({
                    'action': 'timer_tick',
                    'remaining_time': remaining_time,
                    'total_time': self.game_duration
                })
                await asyncio.sleep(1)
                remaining_time -= 1

            if self.is_started:
                await self.next_song()
        except asyncio.CancelledError:
            pass

    async def handle_string_guess(self, guess: str):
        """Handles player's song guess"""
        if not self.current_song:
            return

        # TODO: This code is mostly for solo mode or if the
        # admin of the blind test also participates in the
        # guess = guess.lower().strip()
        # title_match = self.fuzzy_match(guess, self.current_song['title'])
        # artist_match = self.fuzzy_match(guess, self.current_song['artist'])

        # if title_match or artist_match:
        #     points = self.calculate_points(title_match, artist_match)
        #     self.score += points

        #     await self.send_json({
        #         'action': 'guess.correct',
        #         'points': points,
        #         'total_score': self.score,
        #         'song_details': {
        #             'title': self.current_song['title'],
        #             'artist': self.current_song['artist'],
        #         }
        #     })

        #     await self.next_song()
        # else:
        #     await self.send_json({
        #         'action': 'guess.incorrect'
        #     })

    # TODO: This code is mostly for solo mode or if the
        # admin of the blind test also participates in the
    # def fuzzy_match(self, guess, target):
    #     """Simple fuzzy matching - can be improved with more sophisticated algorithms"""
    #     return guess in target.lower()

    async def handle_guess(self, team_id: str, title_match: bool, artist_match: bool):
        """Handles player's song guess"""
        if not self.current_song:
            return

        message = {
            'action': None,
            'team_id': team_id,
            'points': 0
        }

        if title_match or artist_match:
            result = await self.calculate_points(title_match, artist_match)

            message['action'] = 'guess_correct'

            if team_id == self.team_one:
                self.team_one.points += result
                message['points'] = self.team_one.points

            if team_id == self.team_two:
                self.team_two.points += result
                message['points'] = self.team_two.points
        else:
            message['action'] = 'guess_incorrect'
            message['points'] = self.team_one.points if team_id == self.team_one else self.team_two.points

        message['song'] = self.current_song

        print('handle_guess', message)

        group_message = self.base_room_message(
            **{'type': 'game.updates', 'message': message})
        await self.channel_layer.group_send(self.diffusion_group_name, group_message)

        await self.send_json(message)
        await self.next_song()

        # matched = None
        # if title_match:
        #     matched = 'Title'
        # elif artist_match:
        #     matched = 'Artist'
        # await self.register_answer(team_id, matched)
        # await self.update_timeline()
