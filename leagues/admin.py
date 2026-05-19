from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import League, LeagueRegistration, Match


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'game', 'status', 'organizer', 'start_date', 'max_participants']
    list_filter = ['game', 'status', 'format']
    search_fields = ['name', 'organizer__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(LeagueRegistration)
class LeagueRegistrationAdmin(admin.ModelAdmin):
    list_display = ['player', 'league', 'status', 'registered_at']
    list_filter = ['status', 'league__game']
    search_fields = ['player__username', 'league__name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['league', 'player_one', 'player_two', 'winner', 'is_completed']
    list_filter = ['is_completed', 'league__game']
    search_fields = ['player_one__username', 'player_two__username']