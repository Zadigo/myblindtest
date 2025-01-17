import time

from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from songs.models import Artist, PopSong, RapSong, RnBSong, Song

from blindtest.rapidapi.client import Spotify


class SongResource(ModelResource):
    class Meta:
        model = Song


class ArtistResource(ModelResource):
    class Meta:
        model = Artist


@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    list_display = ['name', 'genre', 'spotify_id']
    search_fields = ['name', 'genre']
    resource_class = ArtistResource
    actions = ['update_metadata']

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


@admin.register(Song)
class SongAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'artist', 'genre',
        'difficulty', 'period',
        'decade', 'enriched'
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
