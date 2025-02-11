import celery
from celery.utils.log import get_task_logger
from songs.models import Artist, Song

from blindtest.rapidapi.client import Spotify
from googlesearch import search

logger = get_task_logger(__name__)


@celery.shared_task
def song_information(songs):
    songs = Song.objects.filter(id__in=songs)
    for song in songs:
        pass

    return len(songs)


@celery.shared_task
def wikipedia_information(artist_name):
    """This task searches for the Wikipedia pages for the
    given artist on Google. Both the french and english
    pages are used if provided"""
    try:
        artist = Artist.objects.get(name=artist_name)
    except:
        logger.error(f'Could not get Wikipedia page for: {artist_name}')
        return False
    else:
        base_domain = 'wikipedia.org/wiki/'
        results = list(search(f'{artist_name} Wikipedia', num_results=2))

        candidates = list(filter(lambda x: base_domain in x, results))

        if len(candidates) > 0:
            wikipedia_page = candidates[0]
            return wikipedia_page

        logger.error(f'No Wikipedia url candidates for: {artist_name}')
        return False


@celery.shared_task
def artist_spotify_information(artist_name):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.song_set.filter(year=0).values_list('id', flat=True)

    instance = Spotify(artist_name)
    instance.send()

    try:
        data = instance[0]['data']
    except:
        logger.error(f'Could not get artist details for: {artist_name}')
        return {}
    else:
        artist.spotify_id = data['uri'].split(':')[-1]

        try:
            artist.spotify_avatar = data['visuals']['avatarImage']['sources'][0]['url']
        except:
            logger.error(f'Could not get visuals for: {artist_name}')
            return {}
        artist.save()

    lazy_group = celery.group([
        wikipedia_information.s(artist.name),
        song_information.s(list(songs))
    ])

    songs = lazy_group().get()
    return artist.spotify_id
