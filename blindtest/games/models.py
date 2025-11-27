from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from songs.models import Song
from tvshows.models import TVShow
from django.utils.crypto import get_random_string


class Answer(models.Model):
    """Model representing an answer given by a player
    during a blind test game session"""

    game = models.ForeignKey(
        'Game',
        models.SET_NULL,
        blank=True,
        null=True
    )
    player = models.ForeignKey(
        'Player',
        models.CASCADE
    )
    song = models.ForeignKey(
        Song,
        models.CASCADE,
        blank=True,
        null=True
    )
    tvshow = models.ForeignKey(
        TVShow,
        models.CASCADE,
        blank=True,
        null=True
    )
    title_match = models.BooleanField(
        default=False
    )
    artist_match = models.BooleanField(
        default=False
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_on']
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(song__isnull=False) |
                    models.Q(tvshow__isnull=False)
                ),
                name='song_or_tvshow_not_null'
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(song__title_match=True) |
                    models.Q(artist_match=True)
                ),
                name='either_title_or_artist_match_true'
            )
        ]

    def __str__(self):
        return f'Answer by {self.player.name} for song {self.song.pk}'

    @property
    def both_matched(self):
        return self.title_match and self.artist_match

    @property
    def is_correct(self):
        return self.title_match or self.artist_match


class Player(models.Model):
    """Model representing a player from a 
    blind test game session"""

    game = models.ForeignKey(
        'Game',
        models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        unique=True
    )
    player_id = models.CharField(
        max_length=100,
        unique=True
    )
    position = models.PositiveIntegerField(
        default=1
    )
    color = models.CharField(
        max_length=7,
        default='#000000'
    )
    points = models.PositiveIntegerField(
        default=0
    )
    team = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    correctAnswers = models.JSONField(
        default=list
    )
    speciality = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'position'],
                name='unique_player_position_per_game'
            ),
            models.UniqueConstraint(
                fields=['game', 'name'],
                name='unique_player_name_per_game'
            )
        ]

    def __str__(self):
        return f'Player {self.name}'


class Game(models.Model):
    """Model representing a game session"""

    game_id = models.CharField(
        max_length=100,
        unique=True
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.game_id}'


@receiver(pre_save, sender=Player)
def set_player_position(sender, instance: Player, **kwargs):
    """Sets the position at which the player joins the game"""
    if instance.position == 1:
        qs = Player.objects.filter(game=instance.game)
        last_player = qs.order_by('-position').first()

        if last_player:
            instance.position = last_player.position + 1


@receiver(pre_save, sender=Answer)
def set_player_id(sender, instance: Answer, **kwargs):
    """Sets the player_id field based on the related player"""
    if not instance.player_id:
        instance.player_id = f'player_{get_random_string(12)}'
