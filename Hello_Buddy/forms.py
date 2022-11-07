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

from django import forms

from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
