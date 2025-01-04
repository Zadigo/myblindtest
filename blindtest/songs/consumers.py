import random

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core import exceptions
from songs.api import serializers
from songs.models import Song
from songs.utils import create_token


class SongConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_songs(self):
        return list(Song.objects.all().values_list('id', flat=True))

    @database_sync_to_async
    def get_next_songs(self, excluded_songs):
        qs = Song.objects.exclude(id__in=excluded_songs)
        return list(qs.values_list('id', flat=True))

    @database_sync_to_async
    def get_song(self, song_id):
        try:
            song = Song.objects.get(id=song_id)
            serializer = serializers.SongSerializer(instance=song)
            return serializer.data
        except exceptions.ObjectDoesNotExist:
            raise

    async def connect(self):
        await self.accept()
        connection_token = create_token()
        await self.send_json({'type': 'connection.token', 'token': connection_token})

    async def disconnect(self, close_code):
        await self.close(code=1000)

    async def send_error(self, message, error_type="error"):
        await self.send_json({
            "type": error_type,
            "error": message
        })

    async def receive_json(self, content, **kwargs):
        action = content['type']

        if not action:
            self.send_error()

        if action == 'get.song':
            ids = await self.get_songs()
            random_id = random.choice(ids)
            data = await self.get_song(random_id)
            await self.send_json({
                'type': 'get.song',
                'data': data
            })

        if action == 'next.song':
            ids = await self.get_next_songs(content['exclude'])

            if not ids:
                self.send_json({})
                return None

            random_id = random.choice(ids)
            data = await self.get_song(random_id)
            await self.send_json({
                'type': 'next.song',
                'data': data
            })
