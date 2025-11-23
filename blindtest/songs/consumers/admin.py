from typing import Any, Union

import pyotp
import dataclasses
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.logic import GameLogicMixin, Player
from songs.utils import create_token

DictAny = dict[str, str | int | bool | dict[str, Any]]


class ChannelEventsMixin:
    """This mixin provides generic functions used by the devices
    who are connected the blind test game"""

    # Room for broadcasting game updates
    diffusion_group_name: str = 'blind_test_updates'
    # Room for managing pending connections
    waiting_room_name: str = 'blind_test_waiting_room'
    session_id: str = ''

    device_name: str = 'unknown_device'
    device_id: str = f'unknown_device_id'

    @property
    def indexed_diffusion_group_name(self):
        """Returns the base diffusion group name with
        the unique firebase token in order to identify the group"""
        if self.session_id:
            return f"{self.diffusion_group_name}_{self.session_id}"
        return self.diffusion_group_name

    @property
    def indexed_waiting_room_name(self):
        """Returns the base waiting room name with
        the unique firebase token in order to identify the group"""
        if self.session_id:
            return f"{self.waiting_room_name}_{self.session_id}"
        return self.waiting_room_name

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

    async def accept_device(self, content: dict[str, str | int]):
        """Channels handler for accepting a device into the game"""

    async def disconnect_device(self, content: dict[str, str | int]):
        """Channels handler for disconnecting a device from the game"""

    async def game_started(self, content: dict[str, str | int]):
        """Channels handler for indicating that the game has started"""

    async def game_updates(self, content: dict[str, str | int]):
        """Channels handler for connected devices to receive updates on
        the current game: scores, correct answer, song skipped etc"""

    async def game_disconnected(self, content: dict[str, str | int]):
        """Channels handler to indicate to devices that game has either
        disconnected or simply over"""

    async def update_player(self, content: dict[str, str | int]):
        """Channels handler for updating a player's information"""

    # Old handlers kept for reference

    # async def device_connected(self, content: dict[str, str | int]):
    #     """Channels handler for the devices that are connecting
    #     to the current blind test game"""

    # async def device_disconnected(self, content: dict[str, str | int]):
    #     """Channels handler for the devices that have been disconnected
    #     from the current blind test game"""

    # async def device_accepted(self, content: dict[str, str | int]):
    #     """Channels handler for devices that have been accepted
    #     in a blind test room once the code that room has been verified"""

    # async def device_pending(self, content: dict[str, str | int]):
    #     """Channels handler for devices that are pending
    #     in the wait room. These devices have to send a confirmation
    #     code (pin code) for the correct blind test room to accept them"""

    # async def check_pin_code(self, content: dict[str, str | int]):
    #     """Channels handler for authenticating a pin code to
    #     a blind test game"""


class IndividualBlindTestConsumer(GameLogicMixin, ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from admin devices
    which can then be used to control the blind test game. This consumer handles
    blind test games where each player participates individually as opposed to teams."""

    async def connect(self):
        await self.accept()
        self.session_id = self.scope['url_route']['kwargs']['firebase']
        await self.channel_layer.group_add(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_add(self.indexed_waiting_room_name, self.channel_name)

        await self.send_json({
            'action': 'idle_response',
            'code': self.pin_code,
            'connection_url': f'/{self.session_id}/single-player'
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.indexed_waiting_room_name, self.channel_name)
        await self.close(code=code or 1000)

    async def receive_json(self, content: dict[str, Union[str, int, bool]], **kwargs: Any):
        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

        if action == 'start_game':
            if self.is_started:
                await self.send_error("Game already started")
                return

            self.played_songs.clear()

            self.is_started = True

            await self.channel_layer.group_send(
                self.indexed_diffusion_group_name,
                self.base_room_message(**{'type': 'game.started'})
            )

            await self.send_json({'action': 'game_started'})
            await self.next_song()
        elif action == 'stop_game':
            if not self.is_started:
                await self.send_error("Game not started")
                return

            self.is_started = False

            await self.channel_layer.group_send(
                self.indexed_diffusion_group_name,
                self.base_room_message(**{'type': 'game.stopped'})
            )
        elif action == 'submit_guess':
            if not self.is_started:
                await self.send_error("Game not started")
                return

            player_id = content.get('team_or_player_id', None)
            if player_id is None:
                await self.send_error('No team was provided')
                return

            title_match = content.get('title_match', False)
            artist_match = content.get('artist_match', False)

            message = await self.handle_guess(player_id, title_match, artist_match)
            group_message = self.base_room_message(
                **{
                    'type': 'game.updates',
                    'message': message
                }
            )
            await self.channel_layer.group_send(self.indexed_diffusion_group_name, group_message)

            await self.send_json(message)
            await self.next_song()
        elif action == 'not_guessed':
            if self.is_started and self.current_song:
                # message = {'action': 'guess_incorrect', 'song': self.current_song}
                # await self.send_json(message)

                group_message = self.base_room_message(
                    **{
                        'type': 'game.updates',
                        'message': {'action': 'guess_incorrect', 'song': self.current_song}
                    }
                )
                await self.channel_layer.group_send(self.indexed_diffusion_group_name, group_message)
                await self.next_song()
            else:
                await self.send_error('Game not started or no current song')
        elif action == 'randomize_genre':
            if not self.is_started:
                await self.send_error("Cannot randomize. Game not started")
                return

            temporary_genre = content.get('temporary_genre', None)
            if temporary_genre is None:
                await self.send_error('No temporary genre was provided')
                return

            await self.next_song(temporary_genre=temporary_genre)
        elif action == 'game_settings':
            settings: dict[str, DictAny] = content.get('settings', {})

            if settings is None:
                await self.send_error('No settings were provided')
                return

            self.difficulty = settings.get('difficultyLevel', 'All')
            self.genre = settings.get('songType', 'All')

            self.point_value = settings.get('pointValue', 1)
            self.difficulty_bonus = settings.get('songDifficultyBonus', False)
            self.time_bonus = settings.get('timeBonus', False)
            self.number_of_rounds = content.get('rounds', None)
            self.solo_mode = settings.get('soloMode', False)
            self.admin_plays = settings.get('adminPlays', False)

            self.time_range = settings.get('timeRange', [])
            # self.speed_bonus = settings.get('speedBonus', 0)
            self.time_limit = settings.get('timeLimit', 0)
        else:
            await self.send_error('Invalid action')

    async def accept_device(self, content: dict[str, str | int]):
        # print("Accepting device...", content)

        device_session_id = content['session_id']

        if device_session_id != self.session_id:
            await self.send_error('Invalid session ID for device acceptance')
            return

        device_name = content['device_name']

        if device_name == 'player_smartphone':
            player = Player(**content['player'])
            self._players[content['device_id']] = player
            # self.pending_devices.append((content['device_id'], player))
            await self.send_json({'action': 'device_accepted', 'player': dataclasses.asdict(player), 'players': self.players})

    async def disconnect_device(self, content: dict[str, str | int]):
        device_id = content['device_id']

        if device_id in self._players:
            del self._players[device_id]
        await self.send_json({'action': 'device_disconnected', 'players': self.players})

    async def update_player(self, content):
        player = content.get('player', None)
        if player is None:
            return

        player_id = player.get('id', None)
        if player_id is None:
            return

        if player_id in self._players:
            selected_player = self._players[player_id]
            selected_player.name = player.get('name', selected_player.id)
            # print('Updated players', self._players)
