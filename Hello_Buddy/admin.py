from django.contrib import admin
from .models import Event, HostOfEvent, Profile,Mapping,Key_card
# Register your models here.
# class EventAdmin(admin.ModelAdmin):
#     List_display = ['name', 'place', 'participant', 'date', 'type',"image_relative_url","image_upload"]
admin.site.register(Event)
admin.site.register(HostOfEvent)
admin.site.register(Profile)
admin.site.register(Mapping)
admin.site.register(Key_card)
