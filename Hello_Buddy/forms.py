
from django import forms
from .models import Event
from django.db import models  
from django.forms import fields  


class CreateEventForm(forms.ModelForm):
    date = forms.DateTimeField(
        required=True, label='Date', widget=forms.SelectDateWidget)


    class Meta:
        model = Event
        fields = ['name', 'place', 'participant','date', 'type', "image_upload"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Name"}),
            'place': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Place"}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control', "placeholder ": "image_upload"}),
            'participant': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Participant"}),
            'type': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Type"}),
            }
        
