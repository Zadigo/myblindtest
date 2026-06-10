import datetime
from unittest.mock import Mock

from django.test import TestCase
from songs.completion import Wikipedia, nrj
from songs.models import Artist


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
        mock = Mock()
        type(mock).wikipedia_page = 'https://fr.wikipedia.org/wiki/Gwen_Stefani'
        type(mock).name = 'Gwen Stefani'

        result = nrj(mock)

        self.assertIsNotNone(result)
        self.assertIn('date_of_birth', result)
        self.assertIsInstance(result['date_of_birth'], datetime.date)
