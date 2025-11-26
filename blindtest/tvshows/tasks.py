from celery import shared_task
from celery.utils.log import get_task_logger
from tvshows.models import TVShow
from tvshows.rapidapi import IMDB

logger = get_task_logger(__name__)


@shared_task
def update_tvshows_task(pk: str | int):
    """Fetch and update TV show data from IMDB using RapidAPI"""
    try:
        tvshow = TVShow.objects.get(pk=pk)
    except TVShow.DoesNotExist:
        logger.error(f'TVShow with pk={pk} does not exist.')
        return

    client = IMDB(tvshow.title, 'TV')

    try:
        client.send()
    except Exception as e:
        logger.error(f'Error fetching data for TVShow pk={pk}: {e}')
        return
    else:
        if tvshow.title != client.response_data.get('name'):
            logger.warning(f'Title mismatch for TVShow name={tvshow.title}: local="{tvshow.title}" vs remote="{client.response_data.get("name")}". Skipping update.')
            return 
        
        tvshow.imdb_id = client.response_data.get('id')
        tvshow.image_url = client.response_data.get('image')
        tvshow.save()
        logger.info(f'Successfully updated TVShow pk={pk}.')
    return tvshow.imdb_id
