from django import forms
from .models import Event

class CreateEventForm(forms.ModelForm):
    date = forms.DateTimeField(required=True, label='Date', widget=forms.SelectDateWidget)
    
    class Meta:
        model = Event
        fields = ['name', 'place', 'participant', 'date', 'type']