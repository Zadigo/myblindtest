from django.db import models
from songs.models import Song


class SongStatistic(models.Model):
    song = models.ForeignKey(
        Song
    )
    correct_answer = models.PositiveIntegerField(
        default=0
    )
    no_answer = models.PositiveIntegerField(
        default=0
    )
    modified_on = models.DateTimeField(
        auto_now_add=True
    )
    created_on = models.DateTimeField(
        auto_created=True
    )

    def __str__(self):
        return self.song

    @property
    def percentage_rate(self):
        try:
            return self.correct_answer / self.no_answer
        except ZeroDivisionError:
            return 0
        except Exception:
            return 0
