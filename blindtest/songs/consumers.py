from django.utils.crypto import get_random_string
import asyncio
import dataclasses
import random
from typing import List, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core import exceptions
from django.core.cache import cache
from songs.api import serializers
from songs.models import Song
from songs.processors import FuzzyMatcher
from songs.utils import create_token

# TODO: Ability to use jokers:
# 1. point boost (win 15 points on this specific answer)
# 2. Steal the other team's answer but also double the loss if the answer is incorrect
# 3. Win equaalities, if both team finishes with the same amount of points, the team with this card wins

# Intrigue cards:
# Boost: 1x, 2x, 3x, 4x, 5x


# TODO: "type" is for channels and I should rename them to something
# else when sending messages using send_json


@dataclasses.dataclass
class Team:
    name: str = None
    team_id: int = 1
    points: int = 0
    correct_answers: List[int] = dataclasses.field(default_factory=list)
    answer_times: List[int] = dataclasses.field(default_factory=list)


class ConsumerMixin:
    # TODO: Append the blindtest ID to the group
    # when creating the diffusion group in order
    # to be able to run multiple different blindtests
    diffusion_group_name = 'blind_test_updates'

    async def send_error(self, message, error_type='error'):
        await self.send_json({
            'type': error_type,
            'error': message
        })

    # TODO: Channel make diffusion group

    async def device_connected(self, content):
        """Channels handler for the devices that are connecting
        to the current blind test game"""

    async def device_disconnected(self, content):
        """Channels handler for the devices that have been disconnected
        from the current blind test game"""

    async def game_disconnected(self, content):
        """Channels handler to indicate to devices that game has either
        disconnected or simply over"""

    async def game_updates(self, content):
        """Channels handler for receiving messages on score updates
        on the current blindtest"""


class SongConsumer(ConsumerMixin, AsyncJsonWebsocketConsumer):
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
        self.team_one = Team(team_id=0)
        self.team_two = Team(team_id=1)
        self.team_one_score = 0
        self.team_two_score = 0

        self.is_started = False
        self.current_song: dict[str, Union[str, int]] = None
        self.timer_task: asyncio.Task = None

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
        self.connection_token = None

        self.fuzzy_matcher = FuzzyMatcher()

    @database_sync_to_async
    def get_songs(self, temporary_genre: str = None, exclude: List[int] = []) -> List[int]:
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
    def get_song(self, song_id):
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
                'type': 'game.complete',
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
                'type': 'song.new',
                'song': {
                    'audio_url': self.current_song['audio_url']
                }
            })
        else:
            await self.send_json({
                'type': 'song.new',
                'song': self.current_song
            })

        self.current_round += 1

        if self.number_of_rounds is not None:
            if self.current_round > self.number_of_rounds:
                await self.send_json({
                    'type': 'game.complete',
                    'message': 'Final round complete',
                    'final_scores': {
                        'team1': self.team_one_score,
                        'team2': self.team_two_score
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

        # Use the song's difficulty level to calculate
        # the amount of points that will be used  to
        # add to team's final score
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
                    'type': 'timer.tick',
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
        #         'type': 'guess.correct',
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
        #         'type': 'guess.incorrect'
        #     })

    # TODO: This code is mostly for solo mode or if the
        # admin of the blind test also participates in the
    # def fuzzy_match(self, guess, target):
    #     """Simple fuzzy matching - can be improved with more sophisticated algorithms"""
    #     return guess in target.lower()

    async def handle_guess(self, team: int, title_match: bool, artist_match: bool):
        """Handles player's song guess"""
        if not self.current_song:
            return

        message = {
            'type': None,
            'team_id': team,
            'points': 0
        }

        if title_match or artist_match:
            result = await self.calculate_points(title_match, artist_match)

            message['type'] = 'guess.correct'

            if team == 0:
                self.team_one_score += result
                # TODO: Fully implement the dataclass
                self.team_one.points += result
                message['points'] = self.team_one_score

            if team == 1:
                self.team_two_score += result
                # TODO: Fully implement the dataclass
                self.team_two.points += result
                message['points'] = self.team_two_score
        else:
            message['type'] = 'guess.incorrect'
            message['points'] = self.team_one_score if team == 0 else self.team_two_score

        # TODO: Ensure this works properly
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'game_updates',
            'sender': 'blind_test',
            'updates': message
        })

        await self.send_json(message)
        await self.next_song()

    async def connect(self):
        # Create a diffusion group that will allow other
        # devices to get updates on blind test actual state
        await self.accept()
        # TODO: Channel make diffusion group
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)
        self.connection_token = create_token()
        await self.send_json({'type': 'connection.token', 'token': self.connection_token})

    async def disconnect(self, code):
        # TODO: Channel make diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'game.disconnected',
            'origin': 'blind_test'
        })
        await self.channel_layer.group_discard(self.diffusion_group_name, self.channel_name)

        if self.timer_task:
            self.timer_task.cancel()

        await self.close(code=1000)
        self.is_started = False

    async def receive_json(self, content: dict[str, Union[str, int, bool]], **kwargs):
        action = content.get('type')

        if action is None:
            await self.send_error()
            return

        if action == 'start.game':
            settings = content.get('settings', {})
            self.difficulty = settings.get('game_difficulty', 'All')
            self.genre = settings.get('genre', 'All')

            self.point_value = settings.get('point_value', 1)
            self.difficulty_bonus = settings.get('difficulty_bonus', False)
            self.time_bonus = settings.get('time_bonus', False)
            self.number_of_rounds = content.get('number_of_rounds', None)
            self.solo_mode = settings.get('solo_mode', False)
            self.admin_plays = settings.get('admin_plays', False)

            self.team_one_score = 0
            self.team_two_score = 0
            # TODO: Fully implement the dataclass
            self.team_one.points = 0
            self.team_two.points = 0
            self.played_songs.clear()

            self.is_started = True

            await self.send_json({'type': 'game.started'})
            await self.next_song()
        elif action == 'submit.guess':
            if not self.is_started:
                await self.send_error("Game not started")
                return

            team_id = content.get('team_id', None)
            if team_id is None:
                await self.send_error('No team was provided')
                return

            title_match = content.get('title_match', False)
            artist_match = content.get('artist_match', False)
            await self.handle_guess(team_id, title_match, artist_match)

            # TODO: Use when a string guess is passed
            # guess = content.get('guess', '').strip()
            # if guess:
            #     await self.handle_guess(team_id, title_match, artist_match)
        elif action == 'skip.song':
            if self.is_started and self.current_song:
                await self.next_song()
                await self.send_json({
                    'type': 'song.skipped',
                    # 'song_details': {
                    #     'title': self.current_song['title'],
                    #     'artist': self.current_song['artist'],
                    # }
                })
        elif action == 'randomize.genre':
            # Select a temporary genre within songs, if and only if
            # a global genre is not selected
            temporary_genre = content.get('temporary_genre', None)
            if self.is_started:
                self.next_song(temporary_genre=temporary_genre)
        else:
            self.send_error('Invalid action')

    async def device_connected(self, content):
        await self.send_json({
            'action': 'device.connected',
            **content
        })

    async def device_disconnected(self, content):
        print(content)
        await self.send_json({
            'action': 'device.disconnected',
            **content
        })


class TeamConsumer(ConsumerMixin, AsyncJsonWebsocketConsumer):
    """TODO: Consumer that allows players or a team captain to connect to their team, 
    buzz for a correct answer and receive game updates"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScreenInterfaceConsumer(ConsumerMixin, AsyncJsonWebsocketConsumer):
    """Consumer that allows the game admin to project the actual state
    of the game (scores...) to the actual playing teams. This might require
    the user to have another computer to connect to the endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connection_token = get_random_string(length=20)
        self.update_cache = {}
        self.device = 'projection_screen'

    async def connect(self):
        await self.accept()
        # Register this consumer to the diffusion group in order for
        # it to be able to receive messages from the main blind test game
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)
        await self.send_json({
            'action': 'initiate.connection',
            'connection_token': self.connection_token
        })

        # TODO: Channel make diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'device.connected',
            'origin': self.device,
            'connection_token': self.connection_token
        })

    async def disconnect(self, code):
        # TODO: Channel make diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'device.disconnected',
            'origin': self.device,
            'connection_token': self.connection_token
        })
        await self.channel_layer.group_discard(self.diffusion_group_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        action = content.get('type')

        if action is None:
            self.send_error('An action was not provided')
            return

    async def game_updates(self, content):
        await self.send_json({
            'action': 'game_updates',
            **content
        })

    async def game_disconnected(self, content):
        await self.send_json({
            'action': 'game_disconnected',
            **content
        })
