from django import forms
from .models import Event, EventResult

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_date', 'event_time', 'sport', 'league', 'venue', 'home_team', 'away_team', 'event_status', 'event_description']

    def clean(self):
        # converts into proper python data types, check if the data is valid type, format if needed
        cleaned_data = super().clean()
        home = cleaned_data.get('home_team')
        away = cleaned_data.get('away_team')
        # check if home and away exist(not none) + check if they are the same 
        if home and away and home == away:
            raise forms.ValidationError('Home team and away team must be different.')
        return cleaned_data

class EventResultForm(forms.ModelForm):
    class Meta:
        model = EventResult
        fields = ['home_score', 'away_score', 'notes']