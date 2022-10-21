from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateEventForm
from .models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def home(request):
    all_event = Event.objects.all()
    return render(request, 'Hello_Buddy/home.html', context={'events' : all_event})

def create(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            user = request.user
            test = Event.objects.filter(name=data['name'])
            user.event_set.set(test)
            return redirect('home')
    else:
        form = CreateEventForm()
    context = {'form': form}
    return render(request, 'Hello_Buddy/create_event.html', context)

def aboutus(request):
    return render(request, 'Hello_Buddy/aboutus.html')

def reverse_to_home(self):
    """redirect to homepage"""
    return redirect('home')