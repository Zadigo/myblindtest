import time

from django.contrib import admin, messages
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from songs import tasks
from django.utils.crypto import get_random_string
from songs.models import (AfroSong, Artist, PopArtist, PopSong, RapArtist, RapSong,
                          RnBSong, Song)

from blindtest.rapidapi.client import Spotify


class ArtistForeignKeyWidget(ForeignKeyWidget):
    """Widget that handles the creation of the artist
    in the Artist model when importing songs"""

    def clean(self, value, row=None, **kwargs):
        try:
            artist = super().clean(value, row, **kwargs)
        except:
            artist = Artist.objects.create(name=row['name'])
        return artist


class SongResource(ModelResource):
    artist_name = fields.Field(
        attribute='artist',
        column_name='artist',
        widget=ArtistForeignKeyWidget(Artist, field='name')
    )

    class Meta:
        model = Song
        fields = [
            'artist_name', 'name', 'genre',
            'featured_artists', 'youtube_id',
            'year', 'difficulty'
        ]


class ArtistResource(ModelResource):
    class Meta:
        model = Artist
        fields = [
            'name', 'birthname', 'date_of_birth',
            'spotify_id', 'genre', 'spotify_avatar',
            'wikipedia_page'
        ]


@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    list_display = ['name', 'age', 'genre', 'spotify_id']
    fieldsets = [
        [
            'General',
            {
                'fields': ['name', 'birthname', 'date_of_birth', 'is_group']
            }
        ],
        [
            'Spotify',
            {
                'fields': ['spotify_id', 'spotify_avatar', 'genre']
            }
        ],
        [
            'External links',
            {
                'fields': ['wikipedia_page']
            }
        ]
    ]
    search_fields = ['name', 'genre']
    resource_class = ArtistResource
    list_filter = ['is_group']
    actions = [
        'update_metadata', 'update_from_wikipedia',
        'define_genre_to_base_pop', 'define_genre_to_base_afrobeats'
    ]

    def define_genre_to_base_pop(self, request, queryset):
        queryset.update(genre='Electropop')

    def define_genre_to_base_afrobeats(self, request, queryset):
        queryset.update(genre='Afrobeat')

    def update_metadata(self, request, queryset):
        for artist in queryset:
            tasks.artist_spotify_information.apply_async(
                args=[artist.name], countdown=10)
        messages.success(
            request, f'Scheduled Spotify update for {len(queryset)} artists')

    def update_from_wikipedia(self, request, queryset):
        for artist in queryset:
            tasks.wikipedia_information.apply_async((artist.id,), countdown=10)
        messages.success(
            request, f'Scheduled Wikipedia update for {len(queryset)} artists')


@admin.register(Song)
class SongAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'artist', 'genre',
        'difficulty', 'period',
        'decade'
    ]
    list_filter = ['difficulty']
    search_fields = [
        'name',
        'artist__name',
        'artist__genre'
    ]
    resource_class = SongResource
    actions = [
        'set_difficulty_medium',
        'set_difficulty_difficult',
        'duplicate'
    ]

    def set_difficulty_medium(self, request, queryset):
        queryset.update(difficulty=2)
        messages.success(request, f'Updated {len(queryset)} songs')

    def set_difficulty_difficult(self, request, queryset):
        queryset.update(difficulty=5)
        messages.success(request, f'Updated {len(queryset)} songs')

    def duplicate(self, request, queryset):
        if len(queryset) > 1:
            messages.error(
                request, 'You can only duplicate one song at a time')
            return

        for song in queryset:
            new_name = song.name + " (Copy " + get_random_string(5) + ")"
            Song.objects.create(
                name=new_name,
                artist=song.artist,
                genre=song.genre,
                featured_artists=None,
                youtube_id=song.youtube_id,
                year=song.year,
                difficulty=1
            )
        messages.success(request, f'Duplicated {len(queryset)} songs')


class ProxyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre', 'difficulty']
    search_fields = ['name', 'artist__name', 'artist__genre']


@admin.register(PopSong)
class PopSongAdmin(ProxyModelAdmin):
    pass


@admin.register(RapSong)
class RapSongAdmin(ProxyModelAdmin):
    pass


@admin.register(RnBSong)
class RnBSongAdmin(ProxyModelAdmin):
    pass


@admin.register(AfroSong)
class AfroSongAdmin(ProxyModelAdmin):
    pass


@admin.register(RapArtist)
class RapArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthname', 'date_of_birth', 'astrological_sign']
    # filter_horizontal = ['astrological_sign']
    search_fields = ['name', 'birthname']


@admin.register(PopArtist)
class PopArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthname', 'date_of_birth', 'astrological_sign']
    # filter_horizontal = ['astrological_sign']
    search_fields = ['name', 'birthname']
