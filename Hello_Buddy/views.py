from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateEventForm
from .models import Event, HostOfEvent
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    all_event = Event.objects.all()
    return render(request, 'Hello_Buddy/home.html', context={'events': all_event})


@login_required
def create(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            event = Event()
            event.name = data['name']
            event.place = data['place']
            event.participant = data['participant']
            event.date = data['date']
            event.time = data['time']
            event.type = data['type']
            event.image_upload = data['image_upload']
            event.save()
            
            host = HostOfEvent()
            host.user = user
            host.event = event
            host.save()
            
            return redirect('home')
    else:
        form = CreateEventForm()
    context = {'form': form}
    return render(request, 'Hello_Buddy/create_event.html', context)

def aboutus(request):
    return render(request, 'Hello_Buddy/aboutus.html')


def events_by_category(request, event_category):
    sorted_event = Event.objects.filter(type=event_category)
    context = {'events_in_category': sorted_event}
    return render(
        request,
        'Hello_Buddy/event_by_category.html',
        context
    )


def index(request):
    return render(request, 'events/index.html')

def reverse_to_home(self):
    """redirect to homepage"""
    return redirect('home')
