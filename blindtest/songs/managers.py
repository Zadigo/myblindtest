from django.db import models


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
        return qs.filter(genre__icontains='pop')


class RapSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(genre__icontains='rap') |
            models.Q(genre__icontains='hip hop')
        )


class RnBManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(genre__icontains='rhythm and blues') |
            models.Q(genre__icontains='blues')
        )


class AfroSongManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(genre__icontains='afrobeat') |
            models.Q(genre__icontains='amapiano') |
            models.Q(genre__icontains='african')
        )


class RapArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(genre__icontains='rap') |
            models.Q(genre__icontains='hip hop')
        )


class PopArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(genre__icontains='pop')


class IncompleteArtistManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            models.Q(birthname__isnull=True) |
            models.Q(genre__isnull=True) |
            models.Q(birthname=''),
            is_group=False
        )
