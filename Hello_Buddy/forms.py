from django import forms
from .models import Event, Profile
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm

class MyCustomSignupForm(SignupForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder ": "Email"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'] = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder ": "Password"}))
        self.fields['password2'] = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder ": "Password (again)"}))
    
class MyCustomLoginForm(LoginForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder ": "Password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder ": "Username"}))
        
class MyCustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder ": "Email"}))
        
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
