import dataclasses

from django.core.cache import cache
from django.test import TestCase, override_settings
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from faker.providers import DynamicProvider
from songs.logic.base import BaseGameLogicMixin, Player
from songs.logic.base_models import GameSettings, GameState, SongPossibilities
from songs.models import Song

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


class TestBaseGameLogic(TestCase):
    # fixtures = ['songs']

    def setUp(self):
        cache.clear()
        self.instance = BaseGameLogicMixin()
        self.songs = RandomSong.create_batch(20)

        setattr(
            self.instance,
            'game_settings',
            GameSettings(
                difficultyLevel='All',
                genreSelected='All',
                numberOfChoices=4,
                pointValue=1,
                songDifficultyBonus=False
            )
        )
        setattr(self.instance, 'game_state', GameState(
            current_song={
                'id': 1,
                'difficulty': 3,
                'genre': 'Pop'
            }
        ))

        players = {
            '1': Player(id='1', name='Player 1', points=1),
            '2': Player(id='2', name='Player 2', points=10),
            '3': Player(id='3', name='Player 3', points=5),
            '4': Player(id='4', name='Player 3', points=0)
        }

        self.instance.game_state._players = players
        self.instance.game_state.point_value = 1
        self.instance.game_state.difficulty_bonus = False

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

        song_ids = await self.instance.get_songs()
        self.assertIsInstance(song_ids, list)
        self.assertGreater(len(song_ids), 0)

    async def test_get_songs_with_exclude(self):
        # Since this is a mixin we need to set
        # some of the attributes manually

        song_ids = await self.instance.get_songs(exclude=[1])
        self.assertNotIn(1, song_ids)

    async def test_calculate_points(self):
        self.instance.game_settings.pointValue = 2
        self.instance.game_settings.difficultyBonus = False
        self.instance.game_state.current_song = {
            'id': 1,
            'difficulty': 3
        }

        self.assertIsNotNone(self.instance.game_state.current_song)

        value = await self.instance.calculate_points(title_match=True, artist_match=False)
        self.assertEqual(value, 2)

        value = await self.instance.calculate_points(title_match=False, artist_match=True)
        self.assertEqual(value, 2)

        value = await self.instance.calculate_points(title_match=True, artist_match=True)
        self.assertEqual(value, 4)

        value = await self.instance.calculate_points(title_match=False, artist_match=False)
        self.assertEqual(value, 0)

        self.instance.game_settings.songDifficultyBonus = True

        value = await self.instance.calculate_points(title_match=True, artist_match=False)
        self.assertEqual(value, 6)

    async def test_calculate_multiple_choice_points(self):
        possibilities = SongPossibilities(
            currentChoiceAnswers=[
                {'id': 1, 'name': 'Song 1', 'is_correct_answer': False},
                {'id': 2, 'name': 'Song 2', 'is_correct_answer': True},
                {'id': 3, 'name': 'Song 3', 'is_correct_answer': False},
                {'id': 4, 'name': 'Song 4', 'is_correct_answer': False},
            ],
            playerChoices=[
                {'playerId': '1', 'choiceId': 2},
                {'playerId': '2', 'choiceId': 1},
                {'playerId': '3', 'choiceId': 3},
                {'playerId': '4', 'choiceId': 3}
            ]
        )

        setattr(self.instance, 'song_possibilities', possibilities)
        await self.instance.calculate_multiple_choice_points()

        for key, value in self.instance.game_state._players.items():
            with self.subTest(player=key):
                print(value)
                if key == '1':
                    self.assertEqual(
                        value.points, self.instance.game_state._players[key].points + 1)

    async def test_calculate_loosers_loses_points(self):
        # players = self.instance.game_state._players
        await self.instance.calculate_loosers_loses_points('1', title_match=True)

        print(self.instance.game_state._players)

        # Winner gets points
        self.assertEqual(self.instance.game_state._players['1'].points, 2)
        # Loser loses points
        self.assertEqual(self.instance.game_state._players['2'].points, 8)
        # Loser loses points
        self.assertEqual(self.instance.game_state._players['3'].points, 3)
        # Loser cannot go below 0
        self.assertEqual(self.instance.game_state._players['4'].points, 0)

    def test_player_dataclass(self):
        list = [
            Player(id='1', name='Player 1'),
            Player(id='2', name='Player 2')
        ]

        self.assertIn(Player(id='1', name='Player 1'), list)
        self.assertIn('1', list)
        self.assertTrue('1' == list[0])
        self.assertTrue('Player 1' == list[0])

    def test_properties(self):
        players = {
            '1': Player(id='1', name='Player 1', points=1),
            '2': Player(id='2', name='Player 2', points=10)
        }

        self.instance.game_state._players = players
        self.instance.game_state.point_value = 1
        self.instance.game_state.difficulty_bonus = False

        # setattr(self.instance, '_players', players)

        player_list = self.instance.players
        self.assertIsInstance(player_list, list)
        self.assertEqual(len(player_list), 2)

        for item in player_list:
            with self.subTest(item=item):
                self.assertTrue(dataclasses.is_dataclass(item))

        player_values = self.instance.player_values
        self.assertIsInstance(player_values, dict)
        self.assertEqual(len(player_values), 2)

        for _, item in player_values.items():
            with self.subTest(item=item):
                self.assertIsInstance(item, dict)
                self.assertIn('id', item)
                self.assertIn('name', item)
                self.assertIn('points', item)

    async def test_random_choice_answer(self):
        setattr(self.instance, 'multiple_choice_answers', True)
        setattr(self.instance, 'difficulty', 'All')
        setattr(self.instance, 'genre', 'All')
        setattr(self.instance, 'current_song', 'All')
        setattr(self.instance, 'number_of_choices', 4)

        song_ids = await self.instance.get_songs()
        choices = await self.instance.random_choice_answers(song_ids[-1])
        print(choices)
