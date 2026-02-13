import itertools
import json
from functools import lru_cache

from django.conf import settings
from django.core.cache import cache


class MusicGenre:
    data: dict[str, str] = {}
    genres: list[str] = []

    @lru_cache(maxsize=100)
    def read(self) -> dict[str, str]:
        data = cache.get('music_genres', None)

        if data is None:
            path = getattr(
                settings,
                'GENRES_PATH',
                settings.MEDIA_PATH / 'genres.json'
            )
            with open(path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                cache.set('music_genres', data, timeout=60 * 60 * 24)
        self.data = data
        return self.data

    @classmethod
    def choices(cls):
        instance = cls()
        instance.read()

        main_genres = instance.data.keys()
        genres = [instance.data[key] for key in main_genres]
        items: list[str] = sorted(set(list(itertools.chain(*genres))))
        return [(x, x) for x in items]

    @classmethod
    def default(cls, name: str):
        choices = cls.choices()
        candidate = list(filter(lambda x: x[0] == name, choices))
        if candidate:
            return candidate[0]
        return choices[0]
