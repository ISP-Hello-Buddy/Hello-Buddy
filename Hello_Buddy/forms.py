
from django import forms
from .models import Event
# from bootstrap_datepicker_plus import DateTimePickerInput


class CreateEventForm(forms.ModelForm):
    date = forms.DateTimeField(
        required=True, label='Date', widget=forms.SelectDateWidget)

    class Meta:
        model = Event
        fields = ['name', 'place', 'participant',
                  'date', 'type', "image_upload"]
        # fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'Place': forms.TextInput(attrs={'class': 'form-control'}),
                   'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),

                   }
