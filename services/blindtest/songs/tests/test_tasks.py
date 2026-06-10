import unittest

from django.test import TestCase, override_settings
from songs import tasks


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
