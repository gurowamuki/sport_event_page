from datetime import date, time

import pytest
from django.db import IntegrityError, transaction

from .forms import EventForm
from .models import Event, Sport, Team


@pytest.fixture
def two_teams(db):
    sport = Sport.objects.create(sport_name='Test Sport')
    home = Team.objects.create(team_name='Test Home', sport=sport)
    away = Team.objects.create(team_name='Test Away', sport=sport)
    return sport, home, away


def event_form_data(sport, home, away, **overrides):
    data = {
        'event_date': '2026-08-01',
        'event_time': '18:00',
        'sport': sport.pk,
        'league': '',
        'venue': '',
        'home_team': home.pk,
        'away_team': away.pk,
        'event_status': 'scheduled',
        'event_description': '',
    }
    data.update(overrides)
    return data


# --- form-level validation ---

def test_event_form_rejects_same_home_and_away_team(two_teams):
    sport, home, _away = two_teams
    form = EventForm(data=event_form_data(sport, home, home))

    assert not form.is_valid()
    assert 'Home team and away team must be different.' in form.errors['__all__']


def test_event_form_accepts_different_home_and_away_team(two_teams):
    sport, home, away = two_teams
    form = EventForm(data=event_form_data(sport, home, away))

    assert form.is_valid(), form.errors


# --- DB-level constraint (the model itself has no clean(), so this is the
# only thing stopping a same-team event created outside the form/admin) ---

def test_event_creation_violates_db_constraint_for_same_teams(two_teams):
    sport, home, _away = two_teams

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Event.objects.create(
                event_date=date(2026, 8, 1),
                event_time=time(18, 0),
                sport=sport,
                home_team=home,
                away_team=home,
            )


# --- view behavior ---

@pytest.mark.django_db
def test_event_detail_returns_404_for_missing_event(client):
    response = client.get('/events/999999/')

    assert response.status_code == 404
    assert response.json() == {'error': 'Event not found'}


def test_event_list_includes_created_event(client, two_teams):
    sport, home, away = two_teams
    event = Event.objects.create(
        event_date=date(2026, 8, 1),
        event_time=time(18, 0),
        sport=sport,
        home_team=home,
        away_team=away,
    )

    response = client.get('/events/')

    assert response.status_code == 200
    assert event in response.context['events']
