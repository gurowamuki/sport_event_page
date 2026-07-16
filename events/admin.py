from django.contrib import admin

from .models import Country, City, Venue, Sport, League, Team, Event, EventResult


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'code')
    search_fields = ('country_name', 'code')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country')
    search_fields = ('city_name',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'city', 'capacity')
    search_fields = ('venue_name',)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('sport_name',)
    search_fields = ('sport_name',)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_name', 'season', 'sport', 'country')
    search_fields = ('league_name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'short_name', 'sport', 'city', 'founded_year')
    search_fields = ('team_name', 'short_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'event_time', 'sport', 'home_team', 'away_team', 'event_status')
    search_fields = ('home_team__team_name', 'away_team__team_name')


@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    list_display = ('event', 'home_score', 'away_score')
    search_fields = ('event__home_team__team_name', 'event__away_team__team_name')
