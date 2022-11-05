from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from PIL import Image

import datetime

# Create your models here.

class Event(models.Model):
    
    category = [
        ('Eating', 'Eating'),
        ('Sport', 'Sport'),
        ('Movie', 'Movie'),
        ('Party', 'Party'),
        ('Education', 'Education'),
        ]

    name = models.CharField("Name", max_length = 20)
    place = models.CharField("Place", max_length = 50)
    participant = models.PositiveIntegerField("Participant",default=1, validators=[MinValueValidator(1)])
    date = models.DateField("Date")
    time = models.TimeField("Time", default=datetime.time(00, 00))
    type = models.CharField("Type", max_length = 20, null=True, blank = True, choices=category)
    image_upload = models.ImageField(null = True, blank = True, upload_to='event/images')  
    
    def __str__(self):
        """Return a  string representation of the name event object."""
        return self.name


class HostOfEvent(models.Model):
    
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey('Hello_Buddy.Event', on_delete=models.SET_NULL, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default='...',max_length=50)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.username


