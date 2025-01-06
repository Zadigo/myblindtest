from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from songs.models import PopSong, RapSong, Song


class SongResource(ModelResource):
    class Meta:
        model = Song
    
@admin.register(Song)
class SongAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'artist', 'genre',
        'difficulty', 'period', 'decade'
    ]
    search_fields = ['name', 'artist']
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
    search_fields = ['name', 'artist']


@admin.register(RapSong)
class RapSongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'genre', 'difficulty']
    search_fields = ['name', 'artist']
