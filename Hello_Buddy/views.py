from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CreateEventForm
from .models import Event, HostOfEvent, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateUserForm, UpdateProfileForm


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


def reverse_to_home(self):
    """redirect to homepage"""
    return redirect('home')


@login_required
def profile_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user) # ModelForm
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile) # ModelForm

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile-user')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    user = request.user
    all_event = HostOfEvent.objects.filter(user_id=user) # Event objects
    return render(request, 'Hello_Buddy/profile_user.html', context={
        'events': all_event,
        'profile': user.profile,
        'user_form': user_form,
        'profile_form': profile_form
    })


