import json

from django.urls import reverse, reverse_lazy
from graphene_django.utils.testing import GraphQLTestCase
from rest_framework.test import APITransactionTestCase
from songs.tests.utils import RandomSong


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


class TestGraphQlViews(GraphQLTestCase):
    GRAPHQL_URL = reverse_lazy('graphql')

    def setUp(self):
        self.songs = RandomSong.create_batch(5)

    def test_allsongs(self):
        response = self.query(
            '''
            query {
                allSongs {
                    id
                    name
                    artist {
                        name
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response, response.content)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('allSongs', data['data'])
