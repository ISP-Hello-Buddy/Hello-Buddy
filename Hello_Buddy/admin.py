from django.contrib import admin
from .models import Event
# Register your models here.
# class EventAdmin(admin.ModelAdmin):
#     List_display = ['name', 'place', 'participant', 'date', 'type',"image_relative_url","image_upload"]
admin.site.register(Event)
