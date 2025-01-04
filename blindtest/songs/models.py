import re
from urllib.parse import urlunparse

from django.db import models
from songs import managers, validators
from songs.choices import MusicGenre


class Song(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    genre = models.CharField(
        max_length=100,
        choices=MusicGenre.choices(),
        default=MusicGenre.default('Afrobeat')
    )
    artist = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    youtube = models.URLField(
        blank=True,
        null=True,
        validators=[validators.validate_youtube]
    )
    year = models.PositiveIntegerField(
        default=0,
        validators=[validators.validate_year]
    )
    difficulty = models.IntegerField(
        default=1,
        validators=[validators.validate_difficulty]
    )
    created_on = models.DateField(
        auto_now=True
    )

    class Meta:
        ordering = ['artist']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'artist'],
                name='unique_song_per_artist'
            )
        ]
        indexes = [
            models.Index(
                condition=(
                    models.Q(difficulty=4) |
                    models.Q(difficulty=5)
                ),
                fields=['difficulty'],
                name='diffulty_hard'
            )
        ]

    def __str__(self):
        return f'{self.name}'

    @property
    def video_id(self):
        result = re.search(r'\/embed\/(\w+)', self.youtube)
        if result:
            return result.group(1)
        return None

    @property
    def youtube_watch_link(self):
        return urlunparse((
            'https',
            'www.youtube.com',
            'watch',
            None,
            f'v={self.video_id}',
            None
        ))


class PopSong(Song):
    objects = managers.PopSongManager()

    class Meta:
        ordering = ['artist']
        proxy = True


class RapSong(Song):
    objects = managers.RapSongManager()

    class Meta:
        ordering = ['artist']
        proxy = True
