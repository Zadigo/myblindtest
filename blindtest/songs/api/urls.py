from django.urls.conf import re_path
from songs.api import views

app_name = 'songs_api'

urlpatterns = [
    re_path(
        r'^test$',
        views.test,
        name='test'
    ),
    re_path(
        r'^create$',
        views.CreateSongs.as_view(),
        name='create'
    ),
    re_path(
        r'^genres$',
        views.SongGenres.as_view(),
        name='genres'
    ),
    re_path(
        r'^by-artists$',
        views.SearchSongsAndArtists.as_view(),
        name='search'
    ),
    re_path(
        r'^artists$',
        views.AllArtists.as_view(),
        name='artists'
    ),
    re_path(
        r'^$',
        views.AllSongs.as_view(),
        name='songs'
    )
]
