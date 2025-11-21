from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from tvshows.models import ThemeSong, TVShow
from import_export import fields


class ThemeSongForeignKeyWidget(ForeignKeyWidget):
    """Widget that handles the creation of the TV show
    in the TVShow model when importing songs"""

    def clean(self, value, row=None, **kwargs):
        try:
            tv_show = super().clean(value, row, **kwargs)
        except:
            tv_show = TVShow.objects.create(
                title=row['title'],
                title_fr=row.get('title_fr', '')
            )
        return tv_show


class ThemeSongResource(ModelResource):
    series_name = fields.Field(
        attribute='series',
        column_name='series',
        widget=ThemeSongForeignKeyWidget(TVShow, field='title')
    )

    class Meta:
        model = ThemeSong
        fields = [
            'series_name', 
            'name', 
            'artist',
            'youtube_id',
            'year',
            'difficulty'
        ]


class TVShowResource(ModelResource):
    class Meta:
        model = TVShow
        fields = ['title', 'title_fr']


@admin.register(ThemeSong)
class ThemeSongAdmin(ImportExportModelAdmin):
    list_display = ['series', 'name', 'artist', 'period', 'decade']
    search_fields = ['name', 'artist__name']
    resource_class = ThemeSongResource
    ordering = ['name']


@admin.register(TVShow)
class TVShowAdmin(ImportExportModelAdmin):
    list_display = ['title', 'title_fr']
    search_fields = ['title', 'title_fr']
    resource_class = TVShowResource
    ordering = ['title']
