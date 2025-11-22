from typing import Any, Union

import pyotp
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.consumers.admin import ChannelEventsMixin
from songs.logic import GameLogicMixin
from songs.utils import create_token


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
