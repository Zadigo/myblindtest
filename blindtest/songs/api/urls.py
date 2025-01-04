from django.urls.conf import re_path
from songs.api import views

app_name = 'songs_api'

urlpatterns = [
    re_path(
        r'^create$',
        views.CreateSongs.as_view(),
        name='create'
    ),
    re_path(
        r'^random$',
        views.RandomSong.as_view(),
        name='songs'
    ),
    re_path(
        r'^genres$',
        views.SongGenres.as_view(),
        name='genres'
    ),
    re_path(
        r'^$',
        views.AllSongs.as_view(),
        name='songs'
    )
]
