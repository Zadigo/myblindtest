from games.models import SongStatistic
from django.contrib import admin


@admin.register(SongStatistic)
class SongStatisticAdmin(admin.ModelAdmin):
    list_display = ['song', 'created_on']
    date_hierarchy = 'created_on'
