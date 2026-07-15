# import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
# from django.db import IntegrityError

from django.shortcuts import redirect, render

from .models import Event
from .forms import EventForm

# Creates a new event
@login_required
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def event_create(request):
    if request.method == "POST":
        # creates a form instance with user input
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        # empty form for GET request
        form = EventForm()

    return render(request, 'events/event_create.html', {'form': form})


# returns a list of all events with related data
@ensure_csrf_cookie # sends cookie to client 
@require_http_methods(["GET"])
def event_list(request):
    # select_related to optimize queries by fetching related objects (with join)
    events = (
        Event.objects.select_related('sport', 'league', 'venue', 'home_team', 'away_team').all()
    )

    return render(request, 'events/event_list.html', {'events': events})

# returns details of a single event by ID, with related data
@ensure_csrf_cookie # sends cookie to client 
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

    return render(request, 'events/event_detail.html', {'event': event})

def home(request):
    return render(request, 'events/home.html')

# registers a new user and logs them in
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('event_list')
    else:
        form = UserCreationForm()

    return render(request, 'events/register.html', {'form': form})