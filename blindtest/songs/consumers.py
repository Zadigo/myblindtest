from typing import Union

import pyotp
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.logic import GameLogicMixin
from songs.utils import create_token


class ChannelEventsMixin:
    """This mixin provides generic functions used by the devices
    who are connected the blind test game"""

    # TODO: Append the blindtest ID to the group
    # when creating the diffusion group in order
    # to be able to run multiple different blindtests
    diffusion_group_name: str = 'blind_test_updates'
    waiting_room_name: str = 'blind_test_waiting_room'

    async def send_error(self, message, error_type='error'):
        await self.send_json({
            'action': error_type,
            'message': message
        })

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

    async def setup_firebase(self, content):
        """Channels handler that receives and sets the firebase key
        used for all the devices to read from for the game"""

    async def pin_code(self, content):
        """Channels handler for receiving the pin code"""


class SongConsumer(GameLogicMixin, ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    @property
    def keyed_diffusion_group_name(self):
        """Returns the base diffusion group name with
        the unique firebase token in order to identify the group"""
        if self.connection_token:
            return f"{self.diffusion_group_name}_{self.connection_token}"
        return self.diffusion_group_name

    @property
    def waiting_room(self):
        """Returns the waiting room name which corresponds
        to a room containing devices which have not yet
        been accepted to the blind test"""
        if self.connection_token:
            return f"blind_test_waiting_room_{self.connection_token}"
        return 'blind_test_waiting_room'

    async def connect(self):
        # Create a diffusion group that will allow other
        # devices to get updates on blind test actual state
        await self.accept()
        # TODO: Channel make diffusion group
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)

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
        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

        # steps: idle_connect -> start_game -> game_started

        if action == 'idle_connect':
            # The action waits passively
            # waits for other devices to connect
            await self.send_json({
                'action': 'idle_connect',
                'code': self.code_pin
            })

            # Setup the different parameters for
            # actual coming game
            self.connection_token = content.get('firebase_key', None)

            session: dict[str, str | bool | int] = content.get('session', {})

            team_one = session['teams'][0]
            team_two = session['teams'][1]

            self.team_one.team_id = team_one['id']
            self.team_two.team_id = team_two['id']

            self.team_one.points = 0
            self.team_two.points = 0

            settings: dict[str, str | bool | int] = session.get('settings', {})

            self.difficulty = settings.get('difficultyLevel', 'All')
            self.genre = settings.get('songType', 'All')

            self.point_value = settings.get('pointValue', 1)
            self.difficulty_bonus = settings.get('songDifficultyBonus', False)
            self.time_bonus = settings.get('timeBonus', False)
            self.number_of_rounds = content.get('rounds', None)
            self.solo_mode = settings.get('soloMode', False)
            self.admin_plays = settings.get('adminPlays', False)
            # self.time_range = settings.get('timeRange', [])
            # self.speed_bonus = settings.get('speedBonus', 0)
            # self.time_limit = settings.get('timeLimit', 0)
        elif action == 'start_game':
            self.played_songs.clear()

            self.is_started = True

            await self.send_json({'action': 'game_started'})
            await self.next_song()
        elif action == 'submit_guess':
            if not self.is_started:
                await self.send_error("Game not started")
                return

            team_id = content.get('team_id', None)
            if team_id is None:
                await self.send_error('No team was provided')
                return

            ids = [self.team_one.team_id, self.team_two.team_id]
            if team_id not in ids:
                await self.send_error(f'Team not found: {team_id}')
                return

            title_match = content.get('title_match', False)
            artist_match = content.get('artist_match', False)
            await self.handle_guess(team_id, title_match, artist_match)

            # TODO: Implement handler for last answers
            # await self.send_json({
            #     'action': 'last.answers',
            #     'team_one': await self.team_answers(self.team_one.team_id),
            #     'team_two': await self.team_answers(self.team_two.team_id)
            # })

            # TODO: Use when a string guess is passed
            # guess = content.get('guess', '').strip()
            # if guess:
            #     await self.handle_guess(team_id, title_match, artist_match)
        elif action == 'skip_song':
            if self.is_started and self.current_song:
                await self.next_song()
                await self.send_json({
                    'action': 'song_skipped',
                    # 'song_details': {
                    #     'title': self.current_song['title'],
                    #     'artist': self.current_song['artist'],
                    # }
                })
        elif action == 'randomize_genre':
            # Select a temporary genre within songs, if and only if
            # a global genre is not selected
            temporary_genre = content.get('temporary_genre', None)
            if self.is_started:
                await self.next_song(temporary_genre=temporary_genre)
        else:
            await self.send_error('Invalid action')

    async def device_connected(self, content):
        origin = content['device_id']

        await self.send_json({
            'action': 'device_connected',
            'device_id': origin
        })

        # Send the pin code to the devices connected
        # to the diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'pin.code',
            'origin': 'blind_test',
            'receiver': origin,
            'code': self.code_pin
        })

    async def device_disconnected(self, content):
        await self.send_json({
            'action': 'device_disconnected',
            'device_id': content['device_id']
        })

    async def check_code(self, content):
        code = content.get('code', None)
        origin = content.get('origin', None)

        if code is None:
            await self.send_error('No code pin was provided')
            return

        if not self.current_otp_code:
            await self.send_error('No OTP code is active')
            return

        result = self.current_otp_code.verify(code)
        await self.send_json({'action': 'check_code', 'valid': result})
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'check.code',
            'origin': self.device,
            'code': code
        })


class TelevisionConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """Consumer that allows the game admin to project the actual state
    of the game (scores...) a television screen. This might require
    the user to have another computer or a smart TV"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_id = f'tv_{get_random_string(length=20)}'
        self.device = 'projection_screen'
        self.initial_pin_code: int | None = None

    async def connect(self):
        await self.accept()
        # Register this consumer to the diffusion group in order for
        # it to be able to receive messages from the main blind test game
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)

        await self.send_json({
            'action': 'idle_connect',
            'device_id': self.device_id
        })

        # TODO: Channel make diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'device.connected',
            'origin': self.device,
            'device_id': self.device_id
        })

    async def disconnect(self, code):
        # TODO: Channel make diffusion group
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'device.disconnected',
            'origin': self.device,
            'device_id': self.device_id
        })
        await self.channel_layer.group_discard(self.diffusion_group_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

        if action == 'idle_connect':
            print(content)
        elif action == 'check_code':
            code = content.get('pinCode', None)

            if code is None:
                await self.send_error('No code was provided')
                return

            state = code == self.initial_pin_code
            await self.send_json({'action': 'check_code', 'valid': state})

            if state:
                pass
        else:
            await self.send_error(f'No action was provided: {action}')

    async def game_updates(self, content):
        origin = content.get('origin', None)
        if origin == 'blind_test':
            await self.send_json({
                'action': 'game_updates',
                **content
            })

    async def game_disconnected(self, content):
        origin = content.get('origin', None)
        if origin == 'blind_test':
            await self.send_json({
                'action': 'game_disconnected',
                **content
            })

    async def pin_code(self, content):
        origin = content.get('origin', None)
        if origin == 'blind_test':
            self.initial_pin_code = content['code']


class SmartphoneConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from smartphone devices
    which can then be used to interact with the game. The smartphones are
    used as buzzers. When the user buzzes, it stops the game and the timer which
    then allows the admin to determine if the answer is correct or incorrect."""
