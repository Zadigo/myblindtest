from typing import Any, Union

import pyotp
import dataclasses
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.logic import Player
from songs.consumers.admin import ChannelEventsMixin
from songs.utils import create_token


class TeamSmartphoneConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from smartphone devices
    which can then be used to interact with the game. The smartphones are
    used as buzzers. When the user buzzes, it stops the game and the timer which
    then allows the admin to determine if the answer is correct or incorrect"""


class IndividualPlayerSmartphoneConsumer(ChannelEventsMixin, AsyncJsonWebsocketConsumer):
    """This consumer handles connections specifically from smartphone devices
    which can then be used to interact with the game in single-player mode.
    The smartphones are used as buzzers. When the user buzzes, it stops the game
    and the timer which then allows the admin to determine if the answer is correct or incorrect"""

    player = Player()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_name = 'player_smartphone'
        self.device_id = f'player_{get_random_string(length=10)}'
        self.player.name = self.device_id

    async def connect(self) -> None:
        """Handle a new WebSocket connection from a smartphone player."""
        await self.accept()
        self.session_id = self.scope['url_route']['kwargs']['firebase']
        await self.channel_layer.group_add(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_add(self.indexed_waiting_room_name, self.channel_name)

        await self.send_json({
            'action': 'idle_connect',
            'session_id': self.session_id,
            'player': dataclasses.asdict(self.player)
        })

        group_message = self.base_room_message(
            type='accept.device', player=dataclasses.asdict(self.player))
        await self.channel_layer.group_send(self.indexed_waiting_room_name, group_message)

    async def disconnect(self, code: int) -> None:
        group_message = self.base_room_message(type='disconnect.device')
        await self.channel_layer.group_send(self.indexed_waiting_room_name, group_message)

        await self.channel_layer.group_discard(self.indexed_diffusion_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.indexed_waiting_room_name, self.channel_name)
        await self.close(code=code or 1000)

    async def receive_json(self, content: dict[str, Union[str, int, bool]], **kwargs: Any) -> None:
        action = content.get('action')

        if action is None:
            await self.send_error('No action was provided')
            return

    async def game_started(self, content):
        await self.send_json({'action': 'game_started'})

    async def game_updates(self, content):
        await self.send_json(content['message'])

    async def game_disconnected(self, content):
        await self.send_json({'action': 'game_disconnected'})
