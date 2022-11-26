from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver 

@receiver(post_save, sender=User)
def create_user_key_card(sender, instance, created, **kwargs):
    if created:
        Key_card.objects.create(user=instance)

class Event(models.Model):
    """model for each event"""
    category = [
        ('eating', 'Eating'),
        ('sport', 'Sport'),
        ('movie', 'Movie'),
        ('party', 'Party'),
        ('education', 'Education'),
    ]

    name = models.CharField("Name", max_length=20)
    place = models.CharField("Place", max_length=50)
    participant = models.PositiveIntegerField("Participant",
                                            default=1)
    joined = models.PositiveIntegerField(default=0)
    date = models.DateField("Date")
    time = models.TimeField("Time")
    type = models.CharField("Type", max_length=20,
                            null=True, blank=True, choices=category)
    image_upload = models.ImageField(null=True,
                                     blank=True, upload_to='event/images',
                                     default='event/images/default.jpg')

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
        now = timezone.localtime()
        date = now.date()
        time = now.time()
        return date < self.date or (date == self.date and time < self.time)
    
    def get_absolute_url(self):     
        return reverse('event_detail', kwargs={'pk': self.pk})

    def get_url(self):
        """ Come to main your event """
        return reverse("event",kwargs={"id" : self.id})
    
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
    get_key = models.BooleanField(null=True)
    
    def check_get_key(self):
        """check if user get key or not when event is cloased"""
        if self.get_keys:
            return True
        return False
    
    def get_keys(self):
        """get key of event"""
        if self.check_get_key():
            return Key_card.objects.filter(user=self.user)
        
    def check_par(self):
        """ To check participant and use for create button. """
        return True
    
    def __str__(self):
        return f"user : {self.user} : event : {self.event}"
    
class Key_card(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    num_key = models.IntegerField(name="Key_card", null=True,default=3)
    
    def status_card(self):
        """Check status card of user"""
        return int(self.Key_card) > 0      
    
    def full(self):
        """ check that key card full or not"""
        return self.Key_card >= 3
    
    def __str__(self):
        """Return a  string representation of the name key card object."""
        # return str(self.Key_card)
        return str(self.user.username)
        
class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(default="profile/images/default.jpg",
                               upload_to="profile/images")
    bio = models.TextField(default='...', max_length=50)

    # resizing images
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

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
