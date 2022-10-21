from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
from django import forms
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        # }