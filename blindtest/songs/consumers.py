import asyncio
import datetime
import random

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core import exceptions
from django.utils import timezone
from songs.api import serializers
from songs.models import Song
from songs.utils import create_token
from django.core.cache import cache


class SongConsumer(AsyncJsonWebsocketConsumer):
    difficulty = 'All'
    genre = 'All'
    is_started = False

    @database_sync_to_async
    def get_songs(self, exclude=[]):
        cached_qs = cache.get('songs')

        if cached_qs is None:
            qs = Song.objects.all()
            cache.set('songs', qs, timeout=3600)

        qs = Song.objects.all()

        accepted_values = [
            'All', 'Easy', 'Medium',
            'Semi-Pro', 'Difficult', 'Expert'
        ]
        if self.difficulty not in accepted_values:
            return list(qs.values_list('id', flat=True))

        if self.difficulty != 'All':
            items = accepted_values[1:]
            difficulty_value = items.index(self.difficulty) + 1
            qs = qs.filter(difficulty__gte=difficulty_value)

        if self.genre != 'All':
            qs = qs.filter(genre__icontains=self.genre)

        if exclude:
            qs = qs.exclude(id__in=exclude)

        return list(qs.values_list('id', flat=True))

    # @database_sync_to_async
    # def get_next_songs(self, excluded_songs=[]):
    #     qs = Song.objects.exclude(id__in=excluded_songs)
    #     return list(qs.values_list('id', flat=True))

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

    # async def calculate_score(self, total, point, bonus=0, ratio=0):
    #     result = (point * bonus) * ratio
    #     return total + result

    async def receive_json(self, content, **kwargs):
        action = content['type']

        if not action:
            self.send_error()

        # async def time_calculator():
        #     while True:
        #         d = timezone.now() + timezone.timedelta(seconds=1)
        #         await asyncio.sleep(1)
        #         await self.send_json({'type': 'get.date', 'date': d})

        # async def receive_messages():
        #     pass

        # t1 = asyncio.create_task(time_calculator())
        # t2 = asyncio.create_task(receive_messages())

        # await t1
        # await t2

        if action == 'player.connection':
            pass

        if action == 'start.game':
            self.difficulty = content.get('game_difficulty', 'All')
            self.genre = content.get('genre', 'All')
            self.is_started = True

            self.send_json({
                'type': 'start.game'
            })

        if action == 'get.song':
            exclude = content.get('exclude', [])
            ids = await self.get_songs(exclude=exclude)

            if not ids:
                return await self.send_json({})

            random_id = random.choice(ids)
            data = await self.get_song(random_id)

            await self.send_json({
                'type': 'get.song',
                'song': data
            })
