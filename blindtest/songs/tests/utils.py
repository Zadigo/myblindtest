from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.cache import cache
from django.test import TestCase
from django.urls import re_path
from songs.consumers import admin, smartphone


class WSMixin(TestCase):
    def setUp(self):
        cache.clear()

        self.app = URLRouter([
            re_path(
                r'^ws/songs/(?P<firebase>[a-zA-Z0-9]+)/single-player$',
                admin.AdminConsumer.as_asgi()
            ),
            re_path(
                r'^ws/single-player/(?P<firebase>[a-zA-Z0-9]+)/connect$',
                smartphone.PlayerConsumer.as_asgi()
            )
        ])

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            '/ws/songs/1235abc/single-player'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)
        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()
