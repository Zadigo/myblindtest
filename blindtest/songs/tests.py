import json

from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.cache import cache
from django.test import TestCase
from django.urls import re_path
from songs import consumers
from songs.utils import OTPCode


class TestOTPCreation(TestCase):
    def test_general_structure(self):
        instance = OTPCode()
        code = instance.get_code()
        self.assertIsNotNone(code)
        self.assertTrue(instance.verify(code))


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
        self.assertEqual(response['type'], 'connection.token')
        self.assertIn('token', response)

        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()

    async def test_get_songs_no_filter(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

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
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'Expert',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Verify song difficulty
        song = response['song']
        # "Expert" difficulty should be 1
        self.assertLessEqual(song['difficulty'], 5)

        await instance.disconnect()

    async def test_get_songs_with_genre_filter(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'Zouk'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Verify song genre
        song = response['song']
        self.assertEqual(song['genre'], 'Zouk')

        await instance.disconnect()

    async def test_invalid_message_type(self):
        instance = await self.create_connection()

        await instance.send_json_to({'type': 'invalid.type'})

        # Should receive error response
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'error')

        await instance.disconnect()

    async def test_song_caching(self):
        instance = await self.create_connection()

        # Clear cache to start fresh
        cache.clear()

        # Start game
        await instance.send_json_to({
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Verify cache was set
        cached_songs = cache.get('songs_all_all')
        self.assertIsNotNone(cached_songs)

        await instance.disconnect()

    async def test_correct_answer(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'All',
                'genre': 'All'
            }
        })

        # Start game
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

        # Return a song
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Submit correct guess
        await instance.send_json_to({
            'type': 'submit.guess',
            'team_id': 0,
            # Either the user guessed the title, the artist
            # or both (e.g. both are true)
            'title_match': True,
            'artist_match': False
        })

        # Get score
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'guess.correct')
        self.assertIn('team_id', response)
        self.assertEqual(response['points'], 1)

        # Return the next song
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Submit correct guess
        await instance.send_json_to({
            'type': 'submit.guess',
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
        self.assertEqual(response['type'], 'game.complete')
        self.assertIn('final_scores', response)

        await instance.disconnect()

    async def test_correct_answer_using_song_difficulty_bonus(self):
        instance = await self.create_connection()

        await instance.send_json_to({
            'type': 'start.game',
            'settings': {
                'game_difficulty': 'Easy',
                'genre': 'All',
                'difficulty_bonus': True
            }
        })

        # Start game
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'game.started')

        # Return a song
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'song.new')

        # Submit correct guess
        await instance.send_json_to({
            'type': 'submit.guess',
            'team_id': 0,
            'title_match': True,
            'artist_match': False
        })

        # Get score
        response = await instance.receive_json_from()
        self.assertEqual(response['type'], 'guess.correct')
        # We have two songs, one of difficulty 1 and a second of
        # difficulty 5, so 1 x 1 = 1 and 1 x 5 = 5 so the final
        # score should be either 1 or 5
        self.assertIn(response['points'], [1, 5])
