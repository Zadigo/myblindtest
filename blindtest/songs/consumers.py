from typing import Any, Union

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

    def base_room_message(self, **kwargs: str | int):
        base_message = {
            'device_name': self.device_name,
            'device_id': self.device_id,
            'action': None
        }
        base_message.update(kwargs)
        return base_message

    def is_admin_device(self, expected: str, origin: str | int):
        """Check if the device is an admin device. The admin device is
        considered the one that started the blindtest connection"""
        if isinstance(origin, str) and origin.startswith('blind_test'):
            return origin.startswith(expected)
        return False

    async def send_error(self, message: str, error_type: str = 'error'):
        await self.send_json({
            'action': error_type,
            'message': message
        })

    async def device_connected(self, content: dict[str, str | int]):
        """Channels handler for the devices that are connecting
        to the current blind test game"""

    async def device_disconnected(self, content: dict[str, str | int]):
        """Channels handler for the devices that have been disconnected
        from the current blind test game"""

    async def device_accepted(self, content: dict[str, str | int]):
        """Channels handler for devices that have been accepted
        in a blind test room once the code that room has been verified"""

    async def device_pending(self, content: dict[str, str | int]):
        """Channels handler for devices that are pending
        in the wait room. These devices have to send a confirmation
        code (pin code) for the correct blind test room to accept them"""

    async def game_disconnected(self, content: dict[str, str | int]):
        """Channels handler to indicate to devices that game has either
        disconnected or simply over"""

    async def game_updates(self, content: dict[str, str | int]):
        """Channels handler for connected devices to receive updates on
        the current game: scores, correct answer, song skipped etc"""

    async def check_pin_code(self, content: dict[str, str | int]):
        """Channels handler for authenticating a pin code to
        a blind test game"""

    async def accept_device(self, content: dict[str, str | int]):
        """Channels handler for accepting a device into the game"""


class SongConsumer(GameLogicMixin, ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    @property
    def keyed_diffusion_group_name(self):
        """Returns the base diffusion group name with
        the unique firebase token in order to identify the group"""
        if self.connection_token:
            return f"{self.diffusion_group_name}_{self.connection_token}"
        return self.diffusion_group_name

    async def connect(self):
        # Create a diffusion group that will allow other
        # devices to get updates on blind test actual state
        await self.accept()
        # TODO: Channel make diffusion group
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)

    async def disconnect(self, code):
        # TODO: Channel make diffusion group
        message = self.base_room_message(**{'type': 'game.disconnected'})

        await self.channel_layer.group_send(self.waiting_room_name, message)
        await self.channel_layer.group_send(self.diffusion_group_name, message)

        await self.channel_layer.group_discard(self.waiting_room_name, self.channel_name)
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

        # frontend -> onConnected -> idle_connect
        if action == 'idle_connect':
            print(content)
            self.connection_token = content.get('firebase_key', None)
            # Connect to the waiting room which is seperate from the
            # game room and allows us to send messages to pending connections
            await self.channel_layer.group_add(self.waiting_room_name, self.channel_name)

            # The action waits passively
            # waits for other devices to connect
            await self.send_json({
                'action': 'idle_response',
                'code': self.pin_code
            })

            # Setup the different parameters for
            # actual coming game
            settings: dict[str, str | bool | int] = content.get('settings', {})

            if settings is None:
                await self.send_error('No settings were provided')
                return

            if 'teams' not in settings:
                await self.send_error('Not enough teams to start the game')
                return

            team_one = settings['teams'][0]
            team_two = settings['teams'][1]

            self.team_one.team_id = team_one['id']
            self.team_two.team_id = team_two['id']

            self.team_one.points = 0
            self.team_two.points = 0

            settings: dict[str, str | bool |
                           int] = settings.get('settings', {})

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
                message = {'action': 'song_skipped', 'song': self.current_song}
                await self.send_json(message)

                group_message = self.base_room_message(
                    **{
                        'type': 'game.updates',
                        'message': message
                    }
                )
                await self.channel_layer.group_send(self.diffusion_group_name, group_message)

                await self.next_song()
            else:
                await self.send_error('Game not started or no current song')
        elif action == 'randomize_genre':
            if not self.is_started:
                await self.send_error("Cannot randomize. Game not started")
                return

            # Select a temporary genre within songs, if and only if
            # a global genre is not selected
            temporary_genre = content.get('temporary_genre', None)
            if self.is_started:
                await self.next_song(temporary_genre=temporary_genre)
        else:
            await self.send_error('Invalid action')

    async def device_connected(self, content):
        origin = content['device_id']

        thread = content['thread']

        await self.send_json({
            'action': 'device_connected',
            'device_id': origin
        })

        if thread == 'waiting_room':
            action = content['action']

            if action is None:
                # Recognize that a device was connected
                message = self.base_room_message(**{'type': 'device.pending'})
                await self.channel_layer.group_send(self.waiting_room_name, message)
                self.pending_devices.append(origin)

    async def device_disconnected(self, content):
        await self.send_json({
            'action': 'device_disconnected',
            'device_id': content['device_id']
        })

    async def check_pin_code(self, content):
        origin = content['device_id']
        code = content['code']

        if code is None:
            await self.send_error(f'Connection failed for: {origin}')
            return

        if code == self.connection_token:
            await self.send_json({'action': 'device_accepted', 'message': origin})
            message = self.base_room_message(**{'type': 'device.accepted'})
            await self.channel_layer.group_send(self.waiting_room_name, message)


class TelevisionConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """Consumer that allows the game admin to project the actual state
    of the game (scores...) a television screen. This might require
    the user to have another computer or a smart TV"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_name = 'projection_screen'
        self.device_id = f'tv_{get_random_string(length=20)}'
        # The admin device that accepted the code
        # and to which this device is linked to
        self.admin_device: str | None = None

    async def connect(self):
        await self.accept()

        # Register this consumer to the diffusion group in order for
        # it to be able to receive messages from the main blind test game
        # await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)

        # await self.send_json({
        #     'action': 'idle_connect',
        #     'device_id': self.device_id
        # })

        # # TODO: Channel make diffusion group
        # await self.channel_layer.group_send(self.diffusion_group_name, {
        #     'type': 'device.connected',
        #     'origin': self.device,
        #     'device_id': self.device_id
        # })

    async def disconnect(self, code):
        # TODO: Channel make diffusion group
        message = self.base_room_message(**{'type': 'device.disconnected'})
        await self.channel_layer.group_send(self.diffusion_group_name, message)
        await self.channel_layer.group_discard(self.diffusion_group_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

        if action == 'idle_connect':
            # Subscribe to the waiting room
            await self.channel_layer.group_add(self.waiting_room_name, self.channel_name)

            # Notify the waiting room that a device has connected. There can be instances
            # where the room does not exist (it is created by the admin device)
            message = self.base_room_message(
                **{
                    'type': 'device.connected',
                    'thread': 'waiting_room'
                }
            )

            await self.channel_layer.group_send(self.waiting_room_name, message)
            await self.send_json({'action': 'idle_connect', 'message': self.device_id})
        elif action == 'check_code':
            code = content.get('pinCode', None)

            if code is None:
                await self.send_error('No code was provided')
                return

            # Get the admin device to integrate this device
            # into the game room
            message = self.base_room_message(
                **{'type': 'check.pin.code', 'code': code})
            await self.channel_layer.group_send(self.waiting_room_name, message)
        else:
            await self.send_error(f'No action was provided: {action}')

    async def game_updates(self, content):
        print('TelevisionConsumer', content)
        origin = content['device_id']

        if self.is_admin_device('blind_test', origin):
            await self.send_json(content['message'])

    async def game_disconnected(self, content):
        origin = content['device_id']

        await self.send_json(content['message'])
        # FIXME: If the main admin device sends a message,
        # just return the content
        if self.is_admin_device('blind_test', origin):
            await self.send_json(content['message'])

    async def device_pending(self, content):
        origin = content['device_id']

        if self.is_admin_device('blind_test', origin):
            pass

    async def device_accepted(self, content):
        origin = content['device_id']

        if self.is_admin_device('blind_test', origin):
            self.admin_device = origin
            await self.send_json({'action': 'device_accepted'})
            await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)
            await self.channel_layer.group_discard(self.waiting_room_name, self.channel_name)


class SmartphoneConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from smartphone devices
    which can then be used to interact with the game. The smartphones are
    used as buzzers. When the user buzzes, it stops the game and the timer which
    then allows the admin to determine if the answer is correct or incorrect"""

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.device_name = 'projection_screen'
    #     self.device_id = f'buzz_{get_random_string(length=20)}'
    #     # The admin device that accepted the code
    #     # and to which this device is linked to
    #     self.admin_device: str | None = None

    # async def connect(self):
    #     await super().connect()

    # async def receive_json(self, content: dict[str, str | dict[str, Any]], **kwargs):
    #     action = content.get('action')

    #     if action is None:
    #         await self.send_error('No action was provided')
    #         return

    #     if action == 'idle_connect':
    #         # Subscribe to the waiting room
    #         await self.channel_layer.group_add(self.waiting_room_name, self.channel_name)

    #         # Notify the waiting room that a device has connected. There can be instances
    #         # where the room does not exist (it is created by the admin device)
    #         message = self.base_room_message(
    #             **{
    #                 'type': 'device.connected',
    #                 'thread': 'waiting_room'
    #             }
    #         )

    #         await self.channel_layer.group_send(self.waiting_room_name, message)
    #         await self.send_json({'action': 'idle_connect', 'message': self.device_id})
