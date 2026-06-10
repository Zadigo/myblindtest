from games.models import Answer, Player, Game
from django.contrib import admin


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['song', 'created_on']
    date_hierarchy = 'created_on'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['game', 'player_id']
    date_hierarchy = 'created_on'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_on']
    date_hierarchy = 'created_on'
