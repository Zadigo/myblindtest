import asyncio
import datetime
import json
import unittest
from unittest.mock import Mock, patch

import nltk
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import re_path, reverse
from rest_framework.test import APITransactionTestCase
from songs import tasks, utils
from songs.completion import Wikipedia, nrj
from songs.consumers import admin, smartphone
from songs.models import Artist, Song
from songs.utils import OTPCode
from songs.logic.base import BaseGameLogicMixin

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


class TestUtils(TestCase):
    def test_otp_util(self):
        instance = OTPCode()
        code = instance.get_code()
        self.assertIsNotNone(code)
        self.assertTrue(instance.verify(code))

    def test_astrologic_sign_util(self):
        d = datetime.datetime(year=2000, month=10, day=1)
        sign = utils.astrologic_sign(d.date())
        self.assertEqual(sign, 'Balance')

        # There seems to be a problem when trying to
        # get data for january artists
        dates = [
            (datetime.datetime(year=1996, month=1, day=15).date(), 'Capricorne'),
            (datetime.datetime(year=1996, month=2, day=15).date(), 'Verseau'),
            (datetime.datetime(year=1996, month=3, day=18).date(), 'Poissons')
        ]

        for item, expected in dates:
            with self.subTest(item=item):
                sign = utils.astrologic_sign(item)
                self.assertEqual(sign, expected)


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


class TestAdminConsumer(WSMixin):
    fixtures = ['songs']

    async def test_initial_connection(self):
        instance = await self.create_connection()

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'idle_response')
        self.assertIn('code', response)
        self.assertIn('connection_url', response)

        # Start game
        await instance.send_json_to({'action': 'start_game'})
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')
        self.assertIn('song', response)

        song = response['song']
        self.assertIn('id', song)

        # Submit guess
        await instance.send_json_to({
            'action': 'submit_guess',
            'team_or_player_id': '0',
            'title_match': True,
            'artist_match': False
        })
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'guess_correct', response)
        self.assertIn('player_id', response)
        self.assertEqual(response['points'], 1)

        await instance.disconnect()


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class TestPlayerConsumer(WSMixin):
    async def test_initial_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            '/ws/single-player/1235abc/connect'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'idle_connect')
        self.assertIn('player', response)

        player = response['player']
        self.assertIn('id', player)
        self.assertIn('name', player)

        # Update player
        # FIXME: The channel layer is timoutting here...
        # await instance.send_json_to({
        #     'action': 'update_player',
        #     'name': 'New Player Name'
        # })
        # response = await instance.receive_json_from()

        await instance.disconnect()


class TestRestApiView(APITransactionTestCase):
    fixtures = ['songs']

    def setUp(self):
        self.client = self.client_class()

    def test_get_all_songs(self):
        response = self.client.get(reverse('songs_api:songs'))
        data = response.json()
        self.assertEqual(len(data), 2)

        for item in data:
            with self.subTest(item=item):
                self.assertIn('id', item)
                self.assertIn('artist', item)
                self.assertIn('youtube', item)

    def test_get_all_artists(self):
        response = self.client.get(reverse('songs_api:artists'))
        data = response.json()
        self.assertEqual(len(data), 1)

        for item in data:
            with self.subTest(item=item):
                self.assertIn('id', item)
                self.assertIn('spotify_id', item)

    def test_search(self):
        path = reverse('songs_api:search')
        response = self.client.get(path, data={'q': 'mariah'})
        data = response.json()

        print(data)

        results = data['results']
        self.assertEqual(len(results), 1)

        for item in results:
            with self.subTest(item=item):
                self.assertIn('song_set', item)

    def test_genres(self):
        response = self.client.get(
            reverse('songs_api:genres'),
            data={'q': 'Love'}
        )
        data = response.json()
        self.assertIn('category', data[0])

    def test_artist_automation(self):
        path = reverse('songs_api:artist_automation')
        response = self.client.get(path)
        data = response.json()
        self.assertIn('id', data[0])

        response = self.client.patch(path, data={
            'id': 1,
            'name': 'Mariah Carey',
            'birthname': 'Mariah K Carey',
            'date_of_birth': '1988-1-1'
        })
        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['birthname'], 'Mariah K Carey')

    def test_create_song(self):
        data = [
            {
                'name': 'Julie, Alice, Au Pays',
                'genre': 'Zouk',
                'featured_artists': '',
                'youtube_id': 'abc-d',
                'artist_name': 'Malo',
                'difficulty': 4,
                'year': 2018,
                'wikipedia_page': 'https://fr.wikipedia.org/wiki/Malo_(groupe)'
            }
        ]

        response = self.client.post(
            reverse('songs_api:create'),
            data=data,
            format='json'
        )
        response_data = response.json()
        self.assertIn('items', response_data)
        self.assertIn('errors', response_data)
        self.assertEqual(len(response_data['errors']), 0)
        self.assertEqual(len(response_data['items']), 1)

        for item in response_data['items']:
            with self.subTest(item=item):
                self.assertEqual(item['name'], data[0]['name'])


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class TestCeleryTasks(TestCase):
    fixtures = ['songs']

    def test_artist_spotify_information(self):
        t1 = tasks.artist_spotify_information.apply(args=['Mariah Carey'])
        result = t1.get()
        self.assertIsNotNone(result)
        self.assertIsNotNone(result, str)

    @unittest.skip("Database access does not work in celery task test")
    def test_wikipedia_information(self):
        t1 = tasks.wikipedia_information.apply(args=['Mariah Carey'])
        result = t1.get()
        self.assertIsNotNone(result)
        self.assertIsNotNone(result, str)


class TestCompletion(TestCase):
    fixtures = ['fixtures/artists']

    def test_wikipedia(self):
        artist = Artist.objects.first()

        instance = Wikipedia()
        result = instance.extract_text_from_page(artist)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn('mariah carey', result)

        value = instance.get_date_or_birth(result)
        self.assertIsNotNone(value)
        self.assertIsInstance(value, datetime.date)

    def test_artist_no_wikipedia_page(self):
        mock = Mock()
        type(mock).wikipedia_page = 'https://fr.wikipedia.org/wiki/Gwen_Stefani'
        type(mock).name = 'Gwen Stefani'
        type(mock).birthname = 'Gwen Renée Stefani'
        mock.save = Mock()

        instance = Wikipedia()
        result = instance.extract_text_from_page(mock)
        self.assertIsNotNone(result)

        value = instance.get_date_or_birth(result)
        self.assertIsNotNone(value)

    def test_nrj(self):
        artist = Artist.objects.first()
        result = nrj(artist)

        self.assertIsNotNone(result)
        self.assertIn('date_of_birth', result)
        self.assertIsInstance(result['date_of_birth'], datetime.date)


class TestBaseGameLogic(TestCase):
    fixtures = ['songs']

    def setUp(self):
        self.instance = BaseGameLogicMixin()

    @override_settings(CACHE_TIMEOUT=10)
    def test_load_genres(self):
        genres = self.instance.load_json_genres
        self.assertIsInstance(genres, dict)
        self.assertGreater(len(genres), 0)

    @override_settings(CACHE_TIMEOUT=10)
    def test_genres_categories(self):
        categories = self.instance.genres_categories
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)

    @override_settings(CACHE_TIMEOUT=1)
    async def test_get_songs(self):
        # Since this is a mixin we need to set
        # some of the attributes manually
        setattr(self.instance, 'difficulty', 'All')
        setattr(self.instance, 'genre', 'All')

        song_ids = await self.instance.get_songs()
        self.assertIsInstance(song_ids, list)
        self.assertGreater(len(song_ids), 0)

    async def test_get_songs_with_exclude(self):
        # Since this is a mixin we need to set
        # some of the attributes manually
        setattr(self.instance, 'difficulty', 'All')
        setattr(self.instance, 'genre', 'All')

        song_ids = await self.instance.get_songs()
        song_value = await self.instance.get_song(song_ids[0])
        self.assertIsInstance(song_value, dict)

    async def test_calculate_points(self):
        setattr(self.instance, 'point_value', 2)
        setattr(self.instance, 'difficulty_bonus', False)

        value = await self.instance.calculate_points(title_match=True, artist_match=False)
        self.assertEqual(value, 2)

        value = await self.instance.calculate_points(title_match=False, artist_match=True)
        self.assertEqual(value, 2)

        value = await self.instance.calculate_points(title_match=True, artist_match=True)
        self.assertEqual(value, 4)

        value = await self.instance.calculate_points(title_match=False, artist_match=False)
        self.assertEqual(value, 0)

        setattr(self.instance, 'difficulty_bonus', True)
        setattr(self.instance, 'current_song', {'difficulty': 2})
        value = await self.instance.calculate_points(title_match=True, artist_match=True)
        self.assertEqual(value, 8)
