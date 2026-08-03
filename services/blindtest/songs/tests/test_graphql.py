import json

from graphene_django.utils.testing import GraphQLTestCase

from songs.tests.utils import RandomSong


class TestSongGraphQL(GraphQLTestCase):
    GRAPHQL_URL = '/graphql/'

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
