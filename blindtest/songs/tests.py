import datetime
import json
from unittest.mock import patch

from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.cache import cache
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import re_path, reverse
from rest_framework.test import APITransactionTestCase
from songs import consumers, tasks, utils
from songs.utils import OTPCode


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


class TestSongConsumer(TestCase):
    fixtures = ['songs']

    def setUp(self):
        cache.clear()
        self.app = URLRouter([
            re_path(r'^ws/songs$', consumers.SongConsumer.as_asgi()),
        ])

    async def create_connection(self):
        instance = WebsocketCommunicator(self.app, '/ws/songs')
        state, _ = await instance.connect()

        self.assertTrue(state)

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'connection_token')
        self.assertIn('token', response)

        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()

    async def test_get_songs_no_filter(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        response = await instance.receive_json_from()
        self.assertIn('song', response)
        self.assertIn('id', response['song'])
        self.assertIn('name', response['song'])
        self.assertIn('artist', response['song'])

        await instance.disconnect()

    async def test_get_songs_with_difficulty_filter(self):
        instance = await self.create_connection()

        # Start game with difficulty filter
        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'Expert',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Verify song difficulty
        song = response['song']
        # "Expert" difficulty should be 1
        self.assertLessEqual(song['difficulty'], 5)

        await instance.disconnect()

    async def test_get_songs_with_genre_filter(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'Zouk'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Verify song genre
        song = response['song']
        self.assertEqual(song['genre'], 'Zouk')

        await instance.disconnect()

    async def test_invalid_message_type(self):
        instance = await self.create_connection()

        await instance.send_json_to({'action': 'invalid_type'})

        # Should receive error response
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'error')

        await instance.disconnect()

    async def test_song_caching(self):
        instance = await self.create_connection()

        # Clear cache to start fresh
        cache.clear()

        # Start game
        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Verify cache was set
        # FIXME: Returns None
        cached_songs = cache.get('songs_all_all')
        self.assertIsNotNone(cached_songs)

        await instance.disconnect()

    async def test_correct_answer(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        # Start game
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        # Return a song
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Submit correct guess
        await instance.send_json_to({
            'action': 'submit_guess',
            'team_id': 0,
            # Either the user guessed the title, the artist
            # or both (e.g. both are true)
            'title_match': True,
            'artist_match': False
        })

        # Get score
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'guess_correct')
        self.assertIn('team_id', response)
        self.assertEqual(response['points'], 1)

        # Return the next song
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Submit correct guess
        await instance.send_json_to({
            'action': 'submit_guess',
            'team_id': 0,
            'title_match': True,
            'artist_match': True
        })

        # Get score
        response = await instance.receive_json_from()
        # Got 1 point above plus 2 points for guessing
        # both the title and the artist so 1 + 2 = 3
        self.assertEqual(response['points'], 3)

        # Since we have no more songs left the game is over
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_complete')
        self.assertIn('final_scores', response)

        await instance.disconnect()

    async def test_correct_answer_using_song_difficulty_bonus(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'action': 'start_game',
            'settings': {
                'game_difficulty': 'Easy',
                'genre': 'All',
                'difficulty_bonus': True
            }
        })

        # Start game
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        # Return a song
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Submit correct guess
        await instance.send_json_to({
            'action': 'submit_guess',
            'team_id': 0,
            'title_match': True,
            'artist_match': False
        })

        # Get score
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'guess_correct')
        # We have two songs, one of difficulty 1 and a second of
        # difficulty 5, so 1 x 1 = 1 and 1 x 5 = 5 so the final
        # score should be either 1 or 5
        self.assertIn(response['points'], [1, 5])


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
        response = self.client.get(
            reverse('songs_api:search'),
            data={'q': 'Love'}
        )
        data = response.json()
        print(data)
        # results = data['results']
        # self.assertEqual(len(results), 1)

        # for item in results:
        #     with self.subTest(item=item):
        #         self.assertIn('song_set', item)

    def test_genres(self):
        response = self.client.get(
            reverse('songs_api:genres'),
            data={'q': 'Love'}
        )
        data = response.json()
        self.assertIn('Zouk', data)

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
                'year': 2018
            }
        ]

        response = self.client.post(
            reverse('songs_api:create'),
            data=data,
            format='json'
        )
        response_data = response.json()
        self.assertTrue(len(response_data['items']), 1)

        for item in response_data['items']:
            with self.subTest(item=item):
                self.assertEqual(item['name'], data[0]['name'])


class TestScreenInterfaceConsumer(TransactionTestCase):
    fixtures = ['songs']

    def setUp(self):
        self.app = URLRouter([
            re_path(r'^ws/songs$', consumers.SongConsumer.as_asgi()),
            re_path(r'^ws/connect$', consumers.ScreenInterfaceConsumer.as_asgi())
        ])

    async def create_connections(self):
        conn1 = WebsocketCommunicator(self.app, '/ws/songs')
        conn2 = WebsocketCommunicator(self.app, '/ws/connect')

        state, _ = await conn1.connect()
        self.assertTrue(state)

        # Song consumer
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'connection_token')

        state, _ = await conn2.connect()
        self.assertTrue(state)

        # Team consumer
        response = await conn2.receive_json_from()
        self.assertEqual(response['action'], 'initiate_connection')
        self.assertIn('device_id', response)

        return conn1, conn2

    async def test_connection(self):
        conn1, conn2 = await self.create_connections()
        await conn1.disconnect()
        await conn2.disconnect()

    async def test_game_updates(self):
        conn1, conn2 = await self.create_connections()

        await conn1.send_json_to({'action': 'start_game'})

        # Start game
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'game_started')

        # Return a song
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Submit correct guess
        await conn1.send_json_to({
            'action': 'submit_guess',
            'team_id': 0,
            'title_match': True,
            'artist_match': False
        })

        # Get score
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'device_connected')
        self.assertIn('device_id', response)

        # Get score
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'guess_correct')

        # Get next song
        response = await conn1.receive_json_from()
        self.assertEqual(response['action'], 'song_new')

        # Game updates
        response = await conn2.receive_json_from()
        self.assertEqual(response['action'], 'game_updates')

        await conn1.disconnect()
        await conn2.disconnect()

    # FIXME: Times out
    async def test_device_disconnected(self):
        conn1, conn2 = await self.create_connections()

        response = await conn1.receive_json_from()
        print(response)
        # self.assertIn('device_id', response)

        response = await conn2.receive_json_from()
        print(response)
        # self.assertIn('device_in', response)

        response = await conn1.receive_json_from()
        print(response)
        # self.assertIn('device_connected', response)

        await conn2.disconnect(timeout=5)

        # response = await conn1.receive_json_from()
        # self.assertIn('device_disconnected', response)

        await conn1.disconnect()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class TestCeleryTasks(TestCase):
    fixtures = ['songs']

    def test_artist_spotify_information(self):
        t1 = tasks.artist_spotify_information.apply(args=['Mariah Carey'])
        result = t1.get()
        self.assertIsNotNone(result)
        self.assertIsNotNone(result, str)

    def test_wikipedia_information(self):
        t1 = tasks.wikipedia_information.apply(args=['Mariah Carey'])
        result = t1.get()
        print(result)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result, str)
