from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from songs.models import PopSong, Song, RapSong


class SongResource(ModelResource):
    class Meta:
        model = Song


@admin.register(Song)
class SongAdmin(ImportExportModelAdmin):
    list_display = ['name', 'artist', 'genre']
    search_fields = ['name', 'artist']
    resource_class = SongResource


@admin.register(PopSong)
class PopSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre']
    search_fields = ['name']


@admin.register(RapSong)
class RapSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre']
    search_fields = ['name']
