# from django.db import models
# from django.utils import timezone
#
# EVENT_TYPE = [
#     ('Eatting', 'eatting'),
#     ('Sport', 'sport'),
#     ('Movie', 'movie'),
#     ('Party', 'party'),
#     ('Education', 'education'),
# ]
#
#
# class Event(models.Model):
#     """Class for create event"""
#     event_name = models.CharField(max_length=30)
#     event_start_date = models.DateTimeField('Start Date')
#     event_end_date = models.DateTimeField('End Date')
#     event_participate = models.IntegerField()
#     event_type = models.CharField(choices=EVENT_TYPE)
#
#     def __str__(self):
#         return self.event_name
#
#     def event_available(self):
#         now = timezone.now()
#         return now < self.event_end_date
#
#
# class Participate(models.Model):
#     """Class for see all participate"""
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     username = models.CharField(max_length=200)
#     join = models.IntegerField(default=0)
