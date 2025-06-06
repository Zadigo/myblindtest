import celery
from celery import chain
from celery.utils.log import get_task_logger
from django.db import transaction
from googlesearch import search
from songs.models import Artist, Song
from songs.wikipedia import Wikipedia, nrj

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
    given artist on Google. Both the french and english
    pages are used if provided"""
    try:
        artist = Artist.objects.get(id=artist_id)
    except:
        logger.error('Artist does not exists')
    else:
        instance = Wikipedia()

        text = instance.extract_text_from_page(artist)
        date_of_birth = instance.get_date_or_birth(text)

        logger.warning(f'Found data for: {artist.name}: {instance.metadata}')

        artist.birthname = instance.metadata['birthname']
        artist.date_of_birth = date_of_birth or instance.metadata['date_of_birth']

        artist.save()

        nrj_information.apply_async((artist_id,), countdown=5)

        # chain(
        #     nrj_information.s(artist_id)
        # )

        # chain.apply_async()


@celery.shared_task
def nrj_information(artist_id: int):
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

    # lazy_group = celery.group([
    #     wikipedia_information.s(artist.name),
    #     song_information.s(list(songs))
    # ])

    # songs = lazy_group().get()
    return artist.spotify_id
