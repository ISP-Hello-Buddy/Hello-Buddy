from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateEventForm
from .models import Event, ManyToMany
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    all_event = Event.objects.all()
    return render(request, 'Hello_Buddy/home.html', context={'events' : all_event})

@login_required
def create(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            event = Event()
            event.name = data['name']
            event.place = data['place']
            event.participant = data['participant']
            event.date = data['date']
            event.type = data['type']
            event.save()
            
            many = ManyToMany()
            many.user = user
            many.event = event
            many.save()
            
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