from songs import utils
import re
from urllib.parse import urlunparse

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from songs import managers, validators
from songs.choices import MusicGenre


class Artist(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("The artist's stage name"),
        blank=True,
        null=True
    )
    birthname = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    spotify_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_(
            "ID for the given artist "
            "on Spotify"
        )
    )
    genre = models.CharField(
        max_length=100,
        choices=MusicGenre.choices(),
        default=MusicGenre.default('Afrobeat'),
        help_text=_(
            "The global classification for "
            "the given artist"
        )
    )
    spotify_avatar = models.URLField(
        blank=True,
        null=True
    )
    wikipedia_page = models.URLField(
        blank=True,
        null=True,
        validators=[validators.validate_wikipedia_page]
    )
    created_on = models.DateField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    @property
    def age(self):
        if self.date_of_birth:
            current_date = timezone.now()
            return (current_date.year - self.date_of_birth.year)
        return None

    @cached_property
    def astrological_sign(self):
        return utils.astrologic_sign(self.date_of_birth)


class Song(models.Model):
    artist = models.ForeignKey(
        Artist,
        models.SET_NULL,
        blank=True,
        null=True
    )
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
    featured_artists = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    youtube_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
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

    objects = managers.SongManager()

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

    @property
    def youtube(self):
        return f'https://www.youtube.com/embed/{self.youtube_id}'

    @cached_property
    def period(self):
        if self.year == 0:
            return self.year
        current_year = timezone.now().year
        return current_year - self.year

    @cached_property
    def decade(self):
        if self.year == 0:
            return 0
        return int(self.year / 100)


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


class RnBSong(Song):
    objects = managers.RnBManager()

    class Meta:
        ordering = ['artist']
        verbose_name = 'rhythm and blues song'
        proxy = True
