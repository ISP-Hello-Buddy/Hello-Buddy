from django.db import models
from django.contrib.auth.models import AbstractUser
from Hello_Buddy.models import Event


class User(AbstractUser):
    """Add more fields to default user model."""
    event_set = models.ManyToManyField('Hello_Buddy.Event')

