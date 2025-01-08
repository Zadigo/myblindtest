from django.db import models


class SongManager(models.Manager):
    def get_artists(self):
        from songs.models import Artist
        if self.featured_artists:
            tokens = self.featured_artists.split(',')
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
