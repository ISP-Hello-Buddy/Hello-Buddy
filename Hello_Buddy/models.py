from django.db import models
from django.core.validators import MinValueValidator

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
    participant = models.PositiveIntegerField("Participant", default=1, validators=[MinValueValidator(1)])
    date = models.DateField("Date")
    time = models.TimeField("Time", default=datetime.time(00, 00))
    type = models.CharField("Type", max_length=20, null=True, blank=True, choices=category, default=1)
    image_upload = models.ImageField(null=True, blank=True, upload_to='event/images')
    
    def __str__(self):
        """Return a  string representation of the name event object."""
        return self.name


class HostOfEvent(models.Model):
    
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey('Hello_Buddy.Event', on_delete=models.SET_NULL, null=True)
