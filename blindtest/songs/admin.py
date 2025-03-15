import time

from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from songs import tasks
from import_export import fields
from songs.models import Artist, PopSong, RapSong, RnBSong, Song

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
            'name', 'birth_name', 'date_of_birth',
            'spotify_id', 'genre', 'spotify_avatar'
        ]


@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    list_display = ['name', 'age', 'genre', 'spotify_id']
    fieldsets = [
        [
            'General',
            {
                'fields': ['name', 'birthname', 'date_of_birth']
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
    actions = ['update_metadata', 'update_from_wikipedia']

    def update_metadata(self, request, queryset):
        for artist in queryset:
            instance = Spotify(artist.name)
            instance.send()

            try:
                data = instance[0]['data']
            except:
                time.sleep(5)
                continue
            else:
                artist.spotify_id = data['uri'].split(':')[-1]

                try:
                    artist.spotify_avatar = data['visuals']['avatarImage']['sources'][0]['url']
                except:
                    time.sleep(5)
                artist.save()

    def update_from_wikipedia(self, request, queryset):
        for artist in queryset:
            tasks.wikipedia_information.apply_async((artist.id,), countdown=10)


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
        'set_difficulty_difficult'
    ]

    def set_difficulty_medium(self, request, queryset):
        queryset.update(difficulty=2)
        messages.success(request, f'Updated {len(queryset)} songs')

    def set_difficulty_difficult(self, request, queryset):
        queryset.update(difficulty=5)
        messages.success(request, f'Updated {len(queryset)} songs')


@admin.register(PopSong)
class PopSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre', 'difficulty']
    search_fields = ['name', 'artist__name', 'artist__genre']


@admin.register(RapSong)
class RapSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre', 'difficulty']
    search_fields = ['name', 'artist__name', 'artist__genre']


@admin.register(RnBSong)
class RnBSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre', 'difficulty']
    search_fields = ['name', 'artist__name', 'artist__genre']
