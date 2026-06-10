import dataclasses
from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from songs.logic.base_models import ContentModel
from songs.logic.base import GameLogicMixin

from blindtest.typings import GameActions, TypeContent


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
        """Generates a base message for sending to
        the channels groups with device information

        >>> self.base_room_message(type='game.started', player_id='player_1234')

        Or, if you need to transfer a full message to the group:
        >>> self.base_room_message(**{'type': 'game.started', 'message': {...}})

        The `device_name` and `device_id` of the sender are automatically included in the message.
        """
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

    async def accept_device(self, content: TypeContent):
        """Channels handler for accepting a device into the game"""

    async def disconnect_device(self, content: TypeContent):
        """Channels handler for disconnecting a device from the game"""

    async def game_started(self, content: TypeContent):
        """Channels handler for indicating that the game has started"""

    async def game_updates(self, content: TypeContent):
        """Channels handler for connected devices to receive updates on
        the current game: scores, correct answer, song skipped etc"""

    async def game_disconnected(self, content: TypeContent):
        """Channels handler to indicate to devices that game has either
        disconnected or simply over"""

    async def update_player(self, content: TypeContent):
        """Channels handler for updating a player's information"""

    async def update_player_failed(self, content: TypeContent):
        """Channels handler for notifying that a player's update has failed for
        example because the name is already taken"""

    async def game_paused(self, content: TypeContent):
        """Channels handler to indicate to devices that game has been paused"""

    async def player_submitted_answer(self, content: TypeContent):
        """Channels handler to indicate that a player has submitted an answer
        when using multiple choice answers"""

    async def try_reconnection(self, content: TypeContent):
        """Channels handler to attempt reconnection of a player by their ID"""


class AdminConsumer(GameLogicMixin, ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from admin devices
    which can then be used to control the blind test game. This consumer handles
    blind test games where each player participates individually as opposed to teams."""

    async def connect(self):
        await self.accept()
        self.session_id = self.scope['url_route']['kwargs']['firebase']
        await self.channel_layer.group_add(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_add(self.indexed_waiting_room_name, self.channel_name)

        await self.send_json({
            'action': GameActions.IDLE_RESPONSE.value,
            'code': self.pin_code,
            'connection_url': f'/ws/songs/{self.session_id}/single-player'
        })

    async def disconnect(self, code):
        self.game_state.reset()
        message = self.base_room_message(**{'type': 'game.disconnected'})
        await self.channel_layer.group_send(self.indexed_diffusion_group_name, message)
        await self.channel_layer.group_discard(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.indexed_waiting_room_name, self.channel_name)
        await self.close(code=code or 1000)

    async def receive_json(self, content: TypeContent, **kwargs: Any):
        # model = ContentModel(**content)

        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

        if action == GameActions.START_GAME.value or action == GameActions.NEXT_SONG.value:
            if self.game_state.is_started:
                if action == GameActions.START_GAME.value:
                    await self.send_error("Game already started")
                    return

            if action == GameActions.START_GAME.value:
                self.game_state.reset()
                self.game_state.is_started = True

                await self.channel_layer.group_send(
                    self.indexed_diffusion_group_name,
                    self.base_room_message(**{'type': 'game.started'})
                )

                await self.send_json({'action': GameActions.GAME_STARTED.value})

            await self.next_song()

            message = self.base_room_message(
                **{
                    'type': 'game.updates',
                    'message': {
                        'action': GameActions.NEXT_SONG_LOADED.value
                    }
                }
            )
            await self.channel_layer.group_send(self.indexed_diffusion_group_name, message)
        elif action == GameActions.STOP_GAME.value:
            if not self.game_state.is_started:
                await self.send_error("Game not started")
                return

            self.game_state.is_started = False

            await self.channel_layer.group_send(
                self.indexed_diffusion_group_name,
                self.base_room_message(**{'type': 'game.stopped'})
            )
        elif action == GameActions.SUBMIT_GUESS.value:
            if not self.game_state.is_started:
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
        elif action == GameActions.NOT_GUESSED.value:
            if self.game_state.is_active:
                group_message = self.base_room_message(
                    **{
                        'type': 'game.updates',
                        'message': {
                            'action': GameActions.GUESS_INCORRECT.value, 
                            'song': self.game_state.current_song
                        }
                    }
                )
                await self.channel_layer.group_send(self.indexed_diffusion_group_name, group_message)
                await self.next_song()
            else:
                await self.send_error('Game not started or no current song')
        elif action == GameActions.RANDOMIZE_GENRE.value:
            if not self.game_state.is_started:
                await self.send_error("Cannot randomize. Game not started")
                return

            temporary_genre = content.get('temporary_genre', None)
            if temporary_genre is None:
                await self.send_error('No temporary genre was provided')
                return

            await self.next_song(temporary_genre=temporary_genre)
        elif action == GameActions.GAME_SETTINGS.value:
            settings: dict[str, Any] = content.get('settings', {})

            if settings is None:
                await self.send_error('No settings were provided')
                return

            self.game_settings.config_from_dict(settings)
        elif action == GameActions.PAUSE_GAME.value:
            # TODO: Implement game pausing
            # self.paused = True if not self.paused else False
            # message = self.base_room_message(**{'type': 'game.paused'})
            # await self.channel_layer.group_send(self.indexed_diffusion_group_name, message)
            pass
        elif action == GameActions.RECONNECT_PLAYER.value:
            await self.channel_layer.group_send(
                self.indexed_diffusion_group_name,
                self.base_room_message(**{
                    'type': 'try.reconnection',
                    'game_id': self.session_id,
                    'player_id': content.get('player_id', '')
                })
            )
        else:
            await self.send_error('Invalid action')

    async def accept_device(self, content: TypeContent):
        device_session_id = content['session_id']

        if device_session_id != self.session_id:
            await self.send_error('Invalid session ID for device acceptance')
            return

        device_name = content['device_name']

        if device_name == 'player_smartphone':
            # NOTE: The player is initially creatd on the
            # SmartphoneConsumer and then updated here as
            # a duplicate for admin tracking
            player = self.game_state.add_player(content['player'])

            await self.send_json({
                'action': GameActions.DEVICE_ACCEPTED.value,
                'player': dataclasses.asdict(player),
                'players': self.game_state.player_values
            })

    async def disconnect_device(self, content: TypeContent):
        device_id = content['device_id']
        state = self.game_state.remove_player(device_id)

        if not state:
            await self.send_error('Device not found for disconnection')
            return

        await self.send_json({
            'action': GameActions.DEVICE_DISCONNECTED.value,
            'players': self.game_state.player_values
        })

    async def update_player(self, content: TypeContent):
        updated_player = content.get('player', None)
        if updated_player is None:
            return

        player_id = updated_player.get('id', None)
        if player_id is None:
            return

        if player_id in self.game_state._players:
            selected_player = self.game_state._players[player_id]

            # Check if the updated name is already taken
            updated_name = updated_player.get('name', None)
            if updated_name is not None:
                if updated_name in self.players:
                    message = self.base_room_message(
                        type='update.player.failed',
                        player_id=player_id,
                        message='Name already taken by another player'
                    )
                    await self.channel_layer.group_send(self.indexed_diffusion_group_name, message)
                    return

            selected_player.name = updated_name
            # print('Updated players', self.game_state._players)

    async def player_submitted_answer(self, content: TypeContent):
        print('Admin received player_submitted_answer', content)
        player_id = content.get('player_id', None)
        answer_index = content.get('answer_index', None)

        if player_id is None or answer_index is None:
            return

        message = {
            'action': GameActions.PLAYER_SUBMITTED_ANSWER.value,
            'player_id': player_id,
            'answer_index': answer_index
        }
        self.song_possibilities.playerChoices.append(message)
        await self.send_json(message)

        # Calculate the points of the Admin. The players
        # will know their points slightly before the
        # next song is loaded
        errors = await self.calculate_multiple_choice_points()
        if errors:
            await self.send_error('; '.join(errors))
            return

        await self.send_json({
            'action': GameActions.MULTI_CHOICE_UPDATED_SCORES.value,
            'players': self.game_state.player_values
        })
