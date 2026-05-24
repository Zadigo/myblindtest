import unittest
from songs.choices import MusicGenre
from django.core.cache import cache


class TestMusicGenre(unittest.TestCase):
    def test_read(self):
        genre = MusicGenre()
        data = genre.read()
        self.assertIsInstance(data, dict)
        self.assertIn('African', data)

    def test_read_is_none(self):
        cache.delete('music_genres')
        genre = MusicGenre()
        genre.read()
        self.assertIsNotNone(genre.data)

    def test_choices(self):
        choices = MusicGenre.choices()
        self.assertIsInstance(choices, list)
        self.assertIn(('Afrobeat', 'Afrobeat'), choices)

    def test_default(self):
        default = MusicGenre.default('Afrobeat')
        self.assertEqual(default, ('Afrobeat', 'Afrobeat'))
