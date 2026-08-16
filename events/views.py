from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from django.shortcuts import get_object_or_404, redirect, render

from .models import Event
from .forms import EventForm, EventResultForm

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
        Event.objects.select_related('sport', 'league', 'venue', 'home_team', 'away_team')
        .order_by('event_date', 'event_time')
    )

    return render(request, 'events/event_list.html', {'events': events})

# returns details of a single event by ID, with related data
@ensure_csrf_cookie # sends cookie to client 
@require_http_methods(["GET"])
def event_detail(request, pk):

    try:
        event = (
            Event.objects
            .select_related('sport', 'league', 'venue', 'home_team', 'away_team', 'eventresult')
            .get(pk=pk)
        )
    except Event.DoesNotExist:
        return render(request, 'events/404.html', status=404)

    result = getattr(event, 'eventresult', None)
    return render(request, 'events/event_detail.html', {'event': event, 'result': result})

# edits an existing event
@login_required
@require_http_methods(["GET", "POST"])
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_edit.html', {'form': form, 'event': event})

# deletes an event, along with its result if one was recorded
@login_required
@require_http_methods(["GET", "POST"])
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    result = getattr(event, 'eventresult', None)

    if request.method == "POST":
        if result:
            result.delete()
        event.delete()
        return redirect('event_list')

    return render(request, 'events/event_delete.html', {'event': event, 'result': result})

# records or edits the result for an event
@login_required
@require_http_methods(["GET", "POST"])
def event_result_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    result = getattr(event, 'eventresult', None)

    if request.method == "POST":
        form = EventResultForm(request.POST, instance=result)
        if form.is_valid():
            event_result = form.save(commit=False)
            event_result.event = event
            event_result.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventResultForm(instance=result)

    return render(request, 'events/event_result_form.html', {'form': form, 'event': event})

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