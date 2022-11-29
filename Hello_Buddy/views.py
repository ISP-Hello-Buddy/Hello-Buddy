import base64

import folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim
from django.urls import reverse
from .forms import CreateEventForm, UpdateProfileForm, UpdateUserForm
from .models import Event, HostOfEvent, Mapping, ParticipantOfEvent, Profile


def check_date(user, date, type):
    """ To check date that equal or not """
    try:
        if type == 'parti':
            participant = ParticipantOfEvent.objects.filter(user_id=user)
            for i in participant:
                if i.event.date == date:
                    return True
        else:
            host = HostOfEvent.objects.filter(user_id=user)
            for i in host:
                if i.event.date == date:
                    return True
    except:
        return False


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
    if event_category == 'all':
        all = Event.objects.all()
        if len(all) == 0:
            messages.info(request, 'No event has been created yet.')
            return redirect('home')
        context = {"events_in_category": all}
        return render(request,
                  "Hello_Buddy/event_by_category.html",
                  context)

    sorted_event = Event.objects.filter(type=event_category)
    if len(sorted_event) == 0:
        messages.info(request, 'No event in this category')
        return redirect('home')
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
                    messages.warning(request,
                                     "This location has not on the map location")  # add text error
                    context = {'form': form}
                    return render(request,
                                  'Hello_Buddy/create_event.html', context=context)

                if check_date(user, data['date'], 'host'):
                    messages.info(
                        request, 'You are allow to create 1 event per day. So, choose another day to create event')
                    context = {'form': form}
                    return render(request,
                                  'Hello_Buddy/create_event.html', context=context)

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

                return redirect(reverse('event_category', args=['all']))
            elif "check_place" in request.POST:
                loca = nomi.geocode(data['place'])
                messages.warning(request, f"Location is {loca}")
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
    profile = request.user.profile

    if request.method == "POST":
        if 'delete' in request.POST:
            id = request.POST.get("delete")
            deleted_event = Event.objects.filter(id=id).first()
            deleted_event.delete()

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
               "profile": profile,
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
    try:
        event_active = Event.objects.filter(id=event_id).first().is_active()
        if not event_active:
            messages.error(request, 'Event is already end.')
            return redirect('profile-user')
        event = Event.objects.filter(id=event_id).first()
        all_event = Event.objects.all()

        mp = Mapping.objects.filter(id=event_id).first()
        m = folium.Map(width=425, height=250, location=[
                       mp.lat, mp.lon], zoom_start=16)
        folium.Marker([mp.lat, mp.lon], popup=mp.address).add_to(m)
        m = m._repr_html_()

        all_par = ParticipantOfEvent.objects.all()

        # Host of event are not allow to join their own event
        host = HostOfEvent.objects.all()
        for i in host:
            if i.user == user and i.event.name == event.name:
                event.status = False

        hostevent = HostOfEvent.objects.filter(event_id=id).first()
        # check that participant already join or not
        try:
            existing_par = ParticipantOfEvent.objects.get(event_id=id,
                                                          user_id=user)
        except ParticipantOfEvent.DoesNotExist:
            # new participant

            context = {"event": event, "events": all_event,
                       "pars": all_par, "m": m, 'host': hostevent.user}

            # join click
            if request.method == "POST":
                if check_date(user, event.date, 'parti'):
                    messages.info(
                        request, "You are allow to join 1 event per day. So, choose another event to join.")
                    context = {"event": event, "events": all_event,
                               "pars": all_par, "m": m, 'host': hostevent.user}
                    return render(request, "Hello_Buddy/event.html", context)

                person = ParticipantOfEvent()
                person.event = Event.objects.filter(id=event_id).first()
                person.user = user
                person.save()

                Event.objects.filter(id=event_id).update(
                    joined=F("joined") + 1)
                event = Event.objects.filter(id=event_id).first()

                messages.success(
                    request, f"You already join {event.name} event.")
                context = {"event": event, "par": person, "events": all_event,
                           "pars": all_par, "m": m, 'host': hostevent.user}
        else:
            # already join
            par = ParticipantOfEvent.objects.filter(event_id=id,
                                                    user_id=user).first()

            context = {"event": event, "par": par, "events": all_event,
                       "pars": all_par, "m": m, 'host': hostevent.user}
            if request.method == "POST":
                existing_par.delete()

                Event.objects.filter(id=event_id).update(
                    joined=F("joined") - 1)
                event = Event.objects.filter(id=event_id).first()

                messages.success(
                    request, f"You already cancel {event.name} event.")
                context = {"event": event, "events": all_event,
                           "pars": all_par, "m": m, 'host': hostevent.user}

        return render(request, "Hello_Buddy/event.html", context)
    except:
        messages.error(request, 'Event does not exit.')
        return redirect('home')


def map(request):
    all_obj = Mapping.objects.all()
    list_map_id = []
    list_map = []
    for i in all_obj:
        if i.event.place in list_map_id:
            continue
        list_map_id.append(i.event.place)

    for i in list_map_id:
        same_map = [j for j in all_obj if i == j.event.place]
        list_map.append(same_map)

    m = folium.Map(width=1120, height=650, location=[
                   13.74492, 100.53378], zoom_start=9)
    for i in list_map:
        html = ""
        for mp in i:
            html += f"""
                <h3><center> <a href="/event/{mp.event.id}" target="_blank">
                {mp.event}</a></center></h3>
                <div><center> Place: {mp.address}</center> </div>
                <div><center> </center></div>

                        <div><center> Date: {mp.event.date}</center> </div>
                        <div><center> Time: {mp.event.time}</center> </div>
                        <div><center> Participant: {mp.event.joined}/
                        {mp.event.participant}
                </center> </div>
                <div><center>
                <button class="btn btn-info" type="button"
                onclick="window.open('/event/{mp.event.id}',
                '_blank');" id="myButton">Visit<a href="/event/{mp.event.id}"
                target="_blank"class="button" ></a></button>
                </div></center>

            """

        popup = folium.Popup(folium.Html(html, script=True), max_width=250)
        folium.Marker([mp.lat, mp.lon], popup=popup,
                      tooltip=f"(click for see detail)").add_to(m)
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {'m': m, }
    return render(request, 'Hello_Buddy/map.html', context)


def edit(request, event_id):
    """ edit event feature"""
    user = request.user
    try:
        event = Event.objects.filter(id=event_id).first()
        event_active = event.is_active()
        date = event.date
        if not event_active:
            messages.error(request, 'Event is already end.')
            return redirect('profile-user')
        if request.method == 'POST':
            form = CreateEventForm(request.POST, instance=event)
            nomi = Nominatim(user_agent="hi_buddy")
            if form.is_valid():
                data = form.cleaned_data
                if "edit_event" in request.POST:
                    location = nomi.geocode(data['place'])
                    if not location:
                        messages.warning(request,
                                        "This location has not on the map location")  # add text error
                        context = {'form': form, 'event_id': event_id}
                        return render(request,
                                    'Hello_Buddy/edit.html', context=context)
                        
                    if data['date'] != date:
                        if check_date(user, data['date'], 'host'):
                            messages.info(
                                request, 'You are allow to create 1 event per day. So, choose another day')
                            context = {'form': form, 'event_id': event_id}
                            return render(request,
                                        'Hello_Buddy/edit.html', context=context)
                    
                    form.save()
                    messages.success(request,
                                        "Your event is updated successfully")
                    return redirect(to="profile-user")
                elif "check_place" in request.POST:
                    loca = nomi.geocode(data['place'])
                    messages.warning(request, f"Location is {loca}")
    except:
        messages.error(request, 'Event does not exit.')
        return redirect('home')
                
    form = CreateEventForm(instance=event)
    context = {'form': form, 'event_id': event_id}
    return render(request, 'Hello_Buddy/edit.html', context)
