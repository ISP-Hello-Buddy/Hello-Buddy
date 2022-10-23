from django.db import models
from django.core.validators import MinValueValidator

import datetime

# Create your models here.

class Event(models.Model):

    name = models.CharField("Name",max_length = 20)
    place = models.CharField("Place",max_length = 50)
    participant = models.PositiveIntegerField("Participant",default=1, validators=[MinValueValidator(1)])
    date = models.DateTimeField("Date")
    type = models.CharField("Type",max_length = 20, null=True)

    image_upload = models.ImageField(null = True,blank = True,upload_to='event/images')  