from typing import Any, Union

import pyotp
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.crypto import get_random_string
from songs.consumers.admin import ChannelEventsMixin
from songs.utils import create_token


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
