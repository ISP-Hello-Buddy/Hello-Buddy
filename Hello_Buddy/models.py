from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from geopy.geocoders import Nominatim
import datetime


from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Event(models.Model):
    """model for each event"""
    category = [
        ('eating', 'Eating'),
        ('sport', 'Sport'),
        ('movie', 'Movie'),
        ('party', 'Party'),
        ('education', 'Education'),
    ]

    name = models.CharField("Name", max_length=15)
    place = models.CharField("Place", max_length=30)
    participant = models.PositiveIntegerField("Participant",
                                            default=1)
    joined = models.PositiveIntegerField(default=0)
    date = models.DateField("Date")
    time = models.TimeField("Time")
    type = models.CharField("Type (optional)", max_length=20,
                            null=True, blank=True, choices=category)
    image_upload = models.ImageField('Image upload (optional)' ,null=True,
                                     blank=True, upload_to='event/images',
                                     default='event/images/default_e.jpg')

    def __str__(self):
        """Return a  string representation of the name event object."""
        return self.name

    def full(self):
        """ check that event full or not"""
        return self.participant == self.joined

    def status(self):
        """ host of event are not allow to join their own event"""
        return True
    
    def is_active(self):
        """ Return true if it's not yet time for the event"""
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        return date < self.date or (date == self.date and time < self.time)
        
        
class HostOfEvent(models.Model):
    """model for record user with their own event"""
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE, null=True)
    event = models.ForeignKey('Hello_Buddy.Event',
                              on_delete=models.CASCADE, null=True)


class ParticipantOfEvent(models.Model):
    """model for record user with joined event"""
    user = models.ForeignKey('auth.user',
                             on_delete=models.CASCADE, null=True)
    event = models.ForeignKey('Hello_Buddy.Event',
                              on_delete=models.CASCADE, null=True)

    def check_par(self):
        """ To check participant and use for create button. """
        return True


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(default="profile/images/default_ava.jpg",
                               upload_to="profile/images")
    bio = models.TextField(default='...', max_length=50)

    def __str__(self):
        return self.user.username


class Mapping(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    lat = models.FloatField(name="lat", blank=True, null=True)
    lon = models.FloatField(name="lon", blank=True, null=True)
    address = models.CharField(
        name="address", blank=True, null=True, max_length=300)

    def __str__(self):
        nomi = Nominatim(user_agent="hi_buddy")
        location = nomi.geocode(self.address)
        if not location:
            return "Not_location"
        return location.address
