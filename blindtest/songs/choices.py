import json
from functools import lru_cache
from django.conf import settings
import itertools


class MusicGenre:
    data = {}
    genres = []

    @lru_cache(maxsize=100)
    def read(self) -> dict[str, str]:
        with open(settings.MEDIA_PATH / 'genres.json', mode='r', encoding='utf-8') as f:
            self.data = json.load(f)
            return self.data

    @classmethod
    def choices(cls):
        instance = cls()
        instance.read()

        main_genres = instance.data.keys()
        genres = [instance.data[key] for key in main_genres]
        items = sorted(set(list(itertools.chain(*genres))))
        return [(x, x) for x in items]

    @classmethod
    def default(cls, name):
        choices = cls.choices()
        candidate = filter(lambda x: x == name, choices)
        if candidate:
            return choices[0]
        return choices[0]
