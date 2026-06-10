from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.cache import cache
from django.test import TestCase
from django.urls import re_path
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from faker.providers import DynamicProvider
from songs.consumers import admin, smartphone
from songs.models import Song


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


music_genres_provider = DynamicProvider(
    provider_name='music_genres',
    elements=['Pop', 'Rock', 'Jazz']
)

fake_genres = FakerClass()
fake_genres.add_provider(music_genres_provider)


class RandomSong(DjangoModelFactory):
    class Meta:
        model = Song

    name = Faker('sentence', nb_words=3)
    genre = fake_genres.music_genres()
    year = Faker('year')
    difficulty = Faker('random_int', min=1, max=5)
