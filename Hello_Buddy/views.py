from .forms import UpdateUserForm, UpdateProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateEventForm
from .models import Event, HostOfEvent, ParticipantOfEvent, Profile , Mapping
from django.contrib.auth.decorators import login_required
from django.db.models import F
import folium
from geopy.geocoders import Nominatim


def home(request):
    """Display all event on home page"""
    all_event = Event.objects.all()
    return render(request,
                  "Hello_Buddy/home.html",
                  context={"events": all_event})


def about_us(request):
    """Display information about us"""
    return render(request,
                  "Hello_Buddy/aboutus.html")


def reverse_to_home(request):
    """Redirect to homepage"""
    return redirect("home")


def events_by_category(request, event_category):
    """Sort event by type"""
    sorted_event = Event.objects.filter(type=event_category)
    context = {"events_in_category": sorted_event}
    return render(request,
                  "Hello_Buddy/event_by_category.html",
                  context)

@login_required
def create(request):
    # get user object
    user = request.user
    # check user login
    if not user.is_authenticated:
        return redirect('login')

    # create event and keep into database
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        nomi = Nominatim(user_agent="hi_buddy")
        mapping = Mapping.objects.all()
        if form.is_valid():
            data = form.cleaned_data
            if "create_event" in request.POST:
                location = nomi.geocode(data['place'])
                if not location:
                    form = CreateEventForm()
                    messages.error(request,"This location is not on the map") # add text error
                    context = {'form': form}
                    return render(request, 'Hello_Buddy/create_event.html', context=context)
                lst_address = [ loca.address for loca in mapping]
                if location.address in lst_address:
                    context = {'form': form}
                    messages.error(request,"This location is used")
                    return render(request, 'Hello_Buddy/create_event.html', context=context)

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

                mapping = Mapping()
                mapping.address = location.address
                mapping.lon = float(location.longitude)
                mapping.lat = float(location.latitude)
                mapping.event = event
                mapping.user = user
                mapping.save()

                return redirect('home')
            elif "check_place" in request.POST:
                loca = nomi.geocode(data['place'])
                messages.warning(request,f"Location is {loca}")
    else:
        form = CreateEventForm()
    context = {'form': form}
    return render(request, 'Hello_Buddy/create_event.html', context)


@login_required
def profile_user(request):
    """
    Profile user that users can edit and show history of
    joined and created
    """

    # Create Profile model
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES,
                                         instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            # Update profile
            user_form.save()
            profile_form.save()
            messages.success(request,
             "Your profile is updated successfully")
            return redirect(to="profile-user")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(
            instance=request.user.profile)

    user = request.user
    all_event = HostOfEvent.objects.filter(
        user_id=user)  # Event objects
    joined_events = ParticipantOfEvent.objects.filter(
        user_id=user)
    context = {"events": all_event,
               "joined_events": joined_events,
               "profile": user.profile,
               "user_form": user_form,
               "profile_form": profile_form,
               }
    return render(request, "Hello_Buddy/profile_user.html", 
    context=context)


@login_required
def event(request, event_id):
    """
    Each event page that show information and users can join and 
    leave
    """
    id = event_id
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    all_event = Event.objects.all()

    # Host of event are not allow to join their own event
    host = HostOfEvent.objects.all()
    for i in host:
        if i.user == user and i.event.name == event.name:
            event.status = False

    # check that participant already join or not
    try:
        existing_par = ParticipantOfEvent.objects.get(event_id=id,
        user_id=user)
    except ParticipantOfEvent.DoesNotExist:
        # new participant
        context = {"event": event, "events": all_event}
        if request.method == "POST":
            person = ParticipantOfEvent()
            person.event = Event.objects.filter(id=event_id).first()
            person.user = user
            person.save()

            Event.objects.filter(id=event_id).update(joined=F("joined") + 1)
            event = Event.objects.filter(id=event_id).first()

            context = {"event": event, "par": person, "events": all_event}
    else:
        # already join
        par = ParticipantOfEvent.objects.filter(event_id=id,
                                                user_id=user).first()
        context = {"event": event, "par": par, "events": all_event}
        if request.method == "POST":
            existing_par.delete()

            Event.objects.filter(id=event_id).update(joined=F("joined") - 1)
            event = Event.objects.filter(id=event_id).first()

            context = {"event": event, "events": all_event}

    return render(request, "Hello_Buddy/event.html", context)


def map(request):
    all_obj = Mapping.objects.all()
    m = folium.Map(location=[13.74492, 100.53378], zoom_start=12)
    for i in all_obj:
        folium.Marker([i.lat,i.lon], tooltip=i.event,
                          popup=i.address).add_to(m)
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {'m': m, }
    return render(request, 'Hello_Buddy/map.html', context)
