from enum import unique
from django.db import models
from django.core.validators import MinValueValidator

import datetime

# Create your models here.

class Event(models.Model):

    name = models.CharField(max_length = 50)
    place = models.CharField(max_length = 50)
    participant = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    date = models.DateTimeField()
    type = models.CharField(max_length = 20, null=True)
    
class ManyToMany(models.Model):
    
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey('Hello_Buddy.Event', on_delete=models.SET_NULL, null=True)



