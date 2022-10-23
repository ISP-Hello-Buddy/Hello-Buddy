
from django import forms
from .models import Event
from django.db import models  
from django.forms import fields  
# from bootstrap_datepicker_plus import DateTimePickerInput


class CreateEventForm(forms.ModelForm):
    # name = form.
    date = forms.DateTimeField(
        required=True, label='Date', widget=forms.SelectDateWidget)
    # name = forms.CharField(initial='Your name')
    # email = forms.CharField()

    class Meta:
        model = Event
        fields = ['name', 'place', 'participant','date', 'type', "image_upload"]
        # fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'},),
                   'place': forms.TextInput(attrs={'class': 'form-control'}),
                   'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   }
