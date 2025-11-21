import celery
from celery import chain
from celery.utils.log import get_task_logger
from songs.completion import Wikipedia, nrj
from songs.models import Artist, Song

from blindtest.rapidapi.client import Spotify

logger = get_task_logger(__name__)


@celery.shared_task
def song_information(songs):
    songs = Song.objects.filter(id__in=songs)
    for song in songs:
        pass

    return len(songs)


@celery.shared_task
def wikipedia_information(artist_id: int):
    """This task searches for the Wikipedia pages for the
    given artist on Google and extracts pieces of information. 
    Both the french and english pages are used if provided."""
    try:
        artist = Artist.objects.get(id=artist_id)
    except:
        logger.error('Artist does not exists')
    else:
        instance = Wikipedia()

        text = instance.extract_text_from_page(artist)
        date_of_birth = instance.get_date_or_birth(text)

        logger.warning(f'Found data for: {artist.name}: {instance.metadata}')

        birthname = instance.metadata.get('birthname', None)
        if birthname is not None:
            artist.birthname = instance.metadata['birthname']

        artist.date_of_birth = date_of_birth or instance.metadata['date_of_birth']

        genres = instance.metadata.get('genres', [])
        if genres:
            artist.other_genres = ','.join(str(value).strip().title() for value in genres)
        artist.save()

        nrj_information.apply_async(args=[artist_id], countdown=5)


@celery.shared_task
def nrj_information(artist_id: int):
    """This task searches for the artist's date of birth on NRJ's website
    in case we were not able to find it on Wikipedia."""
    try:
        artist = Artist.objects.get(id=artist_id)
    except:
        logger.error('Artist does not exist')
    else:
        result = nrj(artist)
        if artist.date_of_birth is None:
            artist.date_of_birth = result['date_of_birth']
            artist.save()


@celery.shared_task
def artist_spotify_information(artist_name: str):
    """This task searches for the artist's Spotify ID and avatar"""
    artist = Artist.objects.get(name=artist_name)

    if artist.spotify_id is not None:
        logger.warning(f'Spotify ID already exists for: {artist_name}')
        return artist.spotify_id

    instance = Spotify(artist.name, search_type='artists')
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
    
    songs = artist.song_set.filter(year=0).values_list('id', flat=True)
    return artist.spotify_id


@celery.shared_task
def artist_spotify_overview(spotify_id: str):
    pass
