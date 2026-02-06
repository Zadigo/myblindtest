import unittest
from songs.logic._jokers import TheStealerJoker
from songs.logic.base_models import Player
from faker import Faker

faker = Faker()


class TestJokers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        players = {
            'player1': Player(id='player1', name=faker.name(), points=10, gain=5),
            'player2': Player(id='player2', name=faker.name(), points=10, gain=0)
        }
        self.players = players
        self.player_with_the_stealer = players['player1']

    async def test_joker_the_stealer_joker(self):
        instance = TheStealerJoker(player=self.player_with_the_stealer)

        self.players['player2'].gain = 5
        await instance(song={}, winner_or_looser=self.players['player2'], is_winner=True)

        player_one, player_two = self.players.values()
        self.assertEqual(player_one.points, 15)
        self.assertEqual(player_one.gain, 0)

        self.assertEqual(player_two.points, 5)
        self.assertEqual(player_two.gain, 0)
