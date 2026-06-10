from django.db import models
from songs.choices import MusicGenre


class SongManager(models.Manager):
    def get_featured_artists(self, song_id):
        from songs.models import Artist

        song = self.get(id=song_id)
        if song.featured_artists:
            tokens = song.featured_artists.split(',')
            return Artist.objects.filter(name__in=tokens)
        return []


class PopSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('Pop', [])
        return qs.filter(
            models.Q(genre__in=genres) |
            models.Q(genre__icontains='pop')
        )


class RapSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('Hip hop', [])
        return qs.filter(models.Q(genre__in=genres))


class RnBManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()

        rnb_genres = data.get('R&B and soul', [])
        blues_genres = data.get('Blues', [])
        genres = rnb_genres + blues_genres

        return qs.filter(
            models.Q(genre__in=genres) |
            models.Q(genre__icontains='blues')
        )


class AfroSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('African', [])
        return qs.filter(models.Q(genre__in=genres))
    

class LatinSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('Latin', [])
        return qs.filter(models.Q(genre__in=genres))


class RapArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('Hip hop', [])
        return qs.filter(models.Q(genre__in=genres))


class PopArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        data = MusicGenre().read()
        genres = data.get('Pop', [])
        return qs.filter(
            models.Q(genre__in=genres) |
            models.Q(genre__icontains='pop')
        )


class IncompleteArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(birthname__isnull=True) |
            models.Q(genre__isnull=True) |
            models.Q(birthname=''),
            is_group=False
        )
