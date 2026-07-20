from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)

    # The 'managed = False' option tells Django not to manage the database table for this model.
    class Meta:
        managed = False
        db_table = 'country'

    def __str__(self):
        return self.country_name

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,  # Prevent deletion of a country if it has associated cities
        db_column='_country_id'
    )

    class Meta:
        managed = False
        db_table = 'city'
        unique_together = [['city_name', 'country']]

    def __str__(self):
        return self.city_name

class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=150)
    venue_address = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)]) # Forms allow empty & Database stores NULL
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        db_column='_city_id'
    )

    class Meta:
        managed = False
        db_table = 'venue'

    def __str__(self):
        return self.venue_name

class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=100, unique=True)
    sport_description = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'sport'

    def __str__(self):
        return self.sport_name

class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    league_name = models.CharField(max_length=150)
    season = models.CharField(max_length=20, null=True, blank=True)
    sport = models.ForeignKey(
        Sport,
        on_delete=models.RESTRICT,
        db_column='_sport_id'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        db_column='_country_id',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'league'
        unique_together = [['league_name', 'season']]

    def __str__(self):
        return self.league_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=10, null=True, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    sport = models.ForeignKey(
        Sport,
        on_delete=models.RESTRICT,
        db_column='_sport_id'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        db_column='_city_id',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'team'
        unique_together = [['team_name', 'sport']]

    def __str__(self):
        return self.team_name

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    sport = models.ForeignKey(
        Sport,
        on_delete=models.RESTRICT,
        db_column='_sport_id'
    )
    league = models.ForeignKey(
        League,
        on_delete=models.RESTRICT,
        db_column='_league_id',
        null=True,
        blank=True
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.RESTRICT,
        db_column='_venue_id',
        null=True,
        blank=True
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        db_column='_home_team_id',
        related_name='home_events'
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        db_column='_away_team_id',
        related_name='away_events'
    )
    event_description = models.TextField(null=True, blank=True)
    event_status = models.CharField(
        max_length=20,
        default='scheduled',
        choices=[
            ('scheduled', 'Scheduled'),
            ('live', 'Live'),
            ('finished', 'Finished'),
            ('postponed', 'Postponed'),
            ('cancelled', 'Cancelled'),
        ]
    )

    class Meta:
        managed = False
        db_table = 'event'

    def clean(self):
        if self.home_team_id and self.away_team_id and self.home_team_id == self.away_team_id:
            raise ValidationError('Home team and away team must be different.')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.event_date}"

class EventResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    event = models.OneToOneField(
        Event,
        on_delete=models.RESTRICT,
        db_column='_event_id'
    )
    home_score = models.IntegerField(validators=[MinValueValidator(0)])
    away_score = models.IntegerField(validators=[MinValueValidator(0)])
    notes = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'event_result'
    
    def __str__(self):
        return f"{self.event} → {self.home_score}:{self.away_score}"