from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime

# Create your models here.


class Event(models.Model):
    
    category = [
        ('eating', 'Eating'),
        ('sport', 'Sport'),
        ('movie', 'Movie'),
        ('party', 'Party'),
        ('education', 'Education'),
        ]

    name = models.CharField("Name", max_length = 20)
    place = models.CharField("Place", max_length = 50)
    participant = models.PositiveIntegerField("Participant",default=1, validators=[MinValueValidator(1)])
    joined = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(participant)])
    date = models.DateField("Date")
    time = models.TimeField("Time", default=datetime.time(00, 00))
    type = models.CharField("Type", max_length = 20, null=True, blank = True, choices=category)
    image_upload = models.ImageField(null = True, blank = True, upload_to='event/images', default='event/images/default.jpg')  

    
    def __str__(self):
        """Return a  string representation of the name event object."""
        return self.name
    
    def full(self):
        """ check that event full or not"""
        return self.participant == self.joined
    
    def status(self):
        """ host of event are not allow to join their own event"""
        return True
    
class HostOfEvent(models.Model):
    
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey('Hello_Buddy.Event', on_delete=models.SET_NULL, null=True)
    
class ParticipantOfEvent(models.Model):
    
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey('Hello_Buddy.Event', on_delete=models.SET_NULL, null=True)
    
    def check_par(self):
        """ To check participant and use for create button. """
        return True