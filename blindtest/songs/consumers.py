from typing import Union

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.logic import GameLogicMixin
from songs.utils import create_token


class ChannelEventsMixin:
    # TODO: Append the blindtest ID to the group
    # when creating the diffusion group in order
    # to be able to run multiple different blindtests
    diffusion_group_name = 'blind_test_updates'

    async def send_error(self, message, error_type='error'):
        await self.send_json({
            'action': error_type,
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

    async def update_device_cache(self, content):
        """Channels handler for when a new device is conected to the
        websocket and needs its cache to be populated with the current data"""

    async def apply_cache(self, content):
        """Channels handler for when a new device is conected to the
        websocket and wants to apply the values of the cache"""


class SongConsumer(GameLogicMixin, ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Create a diffusion group that will allow other
        # devices to get updates on blind test actual state
        await self.accept()
        # TODO: Channel make diffusion group
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)
        self.connection_token = create_token()

        await self.send_json({
            'action': 'connection_token',
            'token': self.connection_token,
            'team_one_id': self.team_one.team_id,
            'team_two_id': self.team_two.team_id
        })
    
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

        if action == 'start_game':
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

            title_match = content.get('title_match', False)
            artist_match = content.get('artist_match', False)
            await self.handle_guess(team_id, title_match, artist_match)

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
                self.next_song(temporary_genre=temporary_genre)
        # elif action == 'current_cache':
        #     self.channel_layer.group_send(self.diffusion_group_name, {
        #         'type': 'current.cache',
        #         'cache': content.get('cache')
        #     })
        else:
            await self.send_error('Invalid action')

    async def device_connected(self, content):
        await self.send_json({
            'action': 'device_connected',
            'device_id': content['device_id']
        })

    async def device_disconnected(self, content):
        await self.send_json({
            'action': 'device_disconnected',
            'device_id': content['device_id']
        })

    async def update_device_cache(self, content):
        await self.channel_layer.group_send(self.diffusion_group_name, {
            'type': 'apply.cache',
            'cache': self.game_cache
        })


class ScreenInterfaceConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """Consumer that allows the game admin to project the actual state
    of the game (scores...) to the actual playing teams. This might require
    the user to have another computer to connect to the endpoint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_id = f'dev_{get_random_string(length=20)}'
        self.update_cache = {}
        self.device = 'projection_screen'

    async def connect(self):
        await self.accept()
        # Register this consumer to the diffusion group in order for
        # it to be able to receive messages from the main blind test game
        await self.channel_layer.group_add(self.diffusion_group_name, self.channel_name)

        await self.send_json({
            'action': 'initiate_connection',
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

        if action == 'update_device_cache':
            # When a device connects, diffuse the cache to all devices
            # connected to the websocket in the group
            await self.channel_layer.group_send(self.diffusion_group_name, {
                'type': 'update.device.cache',
                'device_id': content.get('device_id')
            })
        else:
            await self.send_error('No action was provided')

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

    async def apply_cache(self, content):
        await self.send_json({
            'action': 'apply_cache',
            'cache': content.get('cache')
        })
