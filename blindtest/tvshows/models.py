from django.db import models
from songs.models import Artist, AbstractSong
from django.utils.translation import gettext_lazy as _
from blindtest.validators import validate_year
from blindtest.validators import validate_difficulty
from django.dispatch import receiver
from django.db.models.signals import pre_save
from urllib.parse import urlparse, parse_qs


class TVShow(models.Model):
    """A television series that has a theme song"""

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text=_('The title of the television series')
    )
    title_fr = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('The French title of the television series, if applicable')
    )
    imdb_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        help_text=_('The IMDB identifier for the television series')
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('URL to an image representing the television series')
    )
    created_on = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ThemeSong(AbstractSong):
    """A theme song from a television series"""

    series = models.ForeignKey(
        TVShow,
        models.CASCADE,
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('If the theme song has a specific name, enter it here')
    )
    artist = models.ForeignKey(
        Artist,
        models.SET_NULL,
        blank=True,
        null=True,
        help_text=_('The artist who performed the theme song if applicable')
    )
    featured_artists = None
    genre = None

    class Meta:
        ordering = ['series', 'artist']
        constraints = [
            models.UniqueConstraint(
                fields=['series', 'name'],
                name='unique_theme_song_per_series'
            )
        ]

    def __str__(self):
        if self.artist is None or self.name is None:
            return f"Theme song from {self.series.title}"
        return f"{self.name} by {self.artist} from {self.series.title}"


@receiver(pre_save, sender=ThemeSong)
def extract_youtube_id(instance, **kwargs):
    if instance.youtube_id and instance.youtube_id.startswith(('http://', 'https://')):
        parsed_url = urlparse(instance.youtube_id)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed_url.query)
            video_ids = query_params.get('v')

            if video_ids:
                instance.youtube_id = video_ids[0]
        elif parsed_url.hostname == 'youtu.be':
            instance.youtube_id = parsed_url.path.lstrip('/')
