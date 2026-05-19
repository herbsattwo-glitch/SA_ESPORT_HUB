from django.contrib import admin
from .models import Player, ScoutingReport


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'primary_game', 'skill_tier',
        'ranking_points', 'wins', 'losses', 'win_rate'
    ]
    list_filter = ['primary_game', 'skill_tier', 'is_available_for_scouting']
    search_fields = ['user__username', 'user__profile__gamertag']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-ranking_points']

    def win_rate(self, obj):
        return f'{obj.win_rate}%'
    win_rate.short_description = 'Win Rate'


@admin.register(ScoutingReport)
class ScoutingReportAdmin(admin.ModelAdmin):
    list_display = ['player', 'scout', 'overall_rating', 'is_recommended', 'created_at']
    list_filter = ['is_recommended', 'overall_rating']
    search_fields = ['player__user__username', 'scout__username']