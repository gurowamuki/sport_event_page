import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from .models import Event

# Creates a new event
@csrf_exempt # disable CSRF protection (no login required)
@require_http_methods(["POST"])
def event_create(request):
    # Parse JSON body and handle errors
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    required_fields = [
        'event_date', 'event_time', 'sport_id',
        'home_team_id', 'away_team_id'
    ]
    # Check for missing required fields
    missing = [f for f in required_fields if data.get(f) is None]
    if missing:
        return JsonResponse({'error': f'Missing required fields: {missing}'}, status=400)

    # Ensures home and away teams aren't the same.
    if data['home_team_id'] == data['away_team_id']:
        return JsonResponse(
            {'error': 'Home team and away team must be different'},
            status=400
        )
    
    # Create Event in the database
    try:
        event = Event.objects.create(
            event_date=data['event_date'],        
            event_time=data['event_time'],        
            sport_id=data['sport_id'],
            league_id=data.get('league_id'), # optional
            venue_id=data.get('venue_id'), # optional
            home_team_id=data['home_team_id'],
            away_team_id=data['away_team_id'],
            event_description=data.get('event_description', ''), # optional
            event_status=data.get('event_status', 'scheduled'), 
        )
    except IntegrityError as e:
        # Catches FK violations 
        return JsonResponse({'error': f'Database integrity error: {str(e)}'}, status=400)

    # return JSON
    return JsonResponse({
        'event_id': event.event_id,
        'event_date': str(event.event_date),
        'event_time': str(event.event_time),
        'sport_id': event.sport_id,
        'home_team_id': event.home_team_id,
        'away_team_id': event.away_team_id,
        'event_status': event.event_status,
        'message': 'Event created successfully',
    }, status=201)

# returns a list of all events with related data
@require_http_methods(["GET"])
def event_list(request):
    # select_related to optimize queries by fetching related objects (with join)
    events = (
        Event.objects.select_related('sport', 'league', 'venue', 'home_team', 'away_team').all()
    )

    data = [
        {
            'event_id': e.event_id,
            'event_date': str(e.event_date),
            'event_time': str(e.event_time),
            'sport': e.sport.sport_name,
            'league': e.league.league_name if e.league else None,
            'venue': e.venue.venue_name if e.venue else None,
            'home_team': e.home_team.team_name,
            'away_team': e.away_team.team_name,
            'event_status': e.event_status,
        }
        for e in events
    ]

    return JsonResponse({'events': data})

# returns details of a single event by ID, with related data
@require_http_methods(["GET"])
def event_detail(request, pk):

    try:
        event = (
            Event.objects
            .select_related('sport', 'league', 'venue', 'home_team', 'away_team')
            .get(pk=pk)
        )
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

    return JsonResponse({
        'event_id': event.event_id,
        'event_date': str(event.event_date),
        'event_time': str(event.event_time),
        'sport': event.sport.sport_name,
        'league': event.league.league_name if event.league else None,
        'venue': event.venue.venue_name if event.venue else None,
        'home_team': event.home_team.team_name,
        'away_team': event.away_team.team_name,
        'event_description': event.event_description,
        'event_status': event.event_status,
    })
