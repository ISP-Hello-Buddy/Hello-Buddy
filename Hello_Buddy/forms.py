from django import forms
from .models import Event
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput


class CreateEventForm(forms.ModelForm):
    date = forms.DateField(required=True, label='Date', widget=DatePickerInput())
    time = forms.TimeField(required=True, label='Time', widget=TimePickerInput())
    type = forms.Select()


    class Meta:
        model = Event
        fields = ['name', 'place', 'participant', 'date', 'type', 'time', "image_upload"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Name"}),
            'place': forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Place"}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control', "placeholder ": "image_upload"}),
            }
        
