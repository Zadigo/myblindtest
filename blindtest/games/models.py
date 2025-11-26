from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from songs.models import Song


class SongStatistic(models.Model):
    song = models.ForeignKey(
        Song,
        models.CASCADE
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
        return f'{self.song}'

    @property
    def percentage_rate(self):
        try:
            return self.correct_answer / self.no_answer
        except ZeroDivisionError:
            return 0
        except Exception:
            return 0


class Game(models.Model):
    game_id = models.CharField(
        max_length=100
    )
    created_on = models.DateTimeField(
        auto_created=True
    )

    def __str__(self):
        return f'{self.game_id}'


@receiver(pre_save, sender=Game)
def create_token(instance, *kwargs):
    instance.game_id = None
