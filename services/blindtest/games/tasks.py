import pandas
from celery import shared_task
from celery.utils.log import get_task_logger
from games.models import Answer, Game
from songs.models import Song
from django.db import models

logger = get_task_logger(__name__)


@shared_task
def create_answer(game_id: str, song_id: int, player_id: str, title_match: bool, artist_match: bool):
    """Create an answer for a given song and player"""
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        logger.error(f"Song with id {song_id} does not exist.")
        return

    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        logger.error(f"Game with id {game_id} does not exist.")
        return

    answer = Answer.objects.create(
        game=game,
        player_id=player_id,
        song=song,
        title_match=title_match,
        artist_match=artist_match
    )
    logger.info(
        f"Created answer {answer.pk} for player {player_id} and song {song_id}.")
    return answer.pk


@shared_task
def create_game_report(game_id: str):
    """Generate a report for the specified game"""
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        logger.error(f"Game with id {game_id} does not exist.")
        return

    answers = game.answer_set.all().select_related('song', 'player', 'tvshow')

    condition = models.Q('song__isnull')
    logic = models.When(condition, then=models.Value('TV Show'))
    case = models.Case(
        logic,
        default=models.Value('Song'),
        output_field=models.CharField()
    )
    answers = answers.annotate(content_type=case)

    df = pandas.DataFrame(
        answers.values(
            'content_type',
            'player__name',
            'song__name',
            'song__artist__name',
            'song__difficulty',
            'song__year',
            'title_match',
            'artist_match',
            'created_on'
        )
    )

    # 1. Correct answers by player
    report = df.groupby(['player__name', 'content_type']).agg(
        total_answers=pandas.NamedAgg(
            column='created_on', 
            aggfunc='count'
        ),
        correct_title_answers=pandas.NamedAgg(
            column='title_match', 
            aggfunc='sum'
        ),
        correct_artist_answers=pandas.NamedAgg(
            column='artist_match', 
            aggfunc='sum'
        )
    ).reset_index()

    # 2. Correct answers by player per genre

    template = {
        'player_report': report.to_dict(orient='records')
    }

    return template
