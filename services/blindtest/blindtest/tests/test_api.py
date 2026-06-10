from django.test import TestCase as DjangoTestCase
from blindtest.api.spotify import ListPlaylists, Spotify


class TestSpotify(DjangoTestCase):
    def test_access_token_retrieval(self):
        spotify = Spotify()
        access_token = spotify.access_token

        self.assertIsNotNone(access_token)
        self.assertIsInstance(access_token, str)

    def test_list_playlists(self):
        spotify = ListPlaylists()
        response = spotify.send()
        print(response)
        # self.assertIsNotNone(response)
        # self.assertIn('items', response)
        # self.assertIsInstance(response['items'], list)

    def test_get_playlist(self):
        spotify = Spotify()
        # Replace with a valid playlist ID for testing
        playlist_id = '3cEYpjA9oz9GiPac4AsH4n'
        response = spotify.send(f'/playlists/{playlist_id}')
        print(response)
        # self.assertIsNotNone(response)
        # self.assertIn('id', response)
        # self.assertEqual(response['id'], playlist_id)
