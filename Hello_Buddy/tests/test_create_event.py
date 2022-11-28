from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Event, HostOfEvent
import datetime


class CreateEventTest(TestCase):
    
    def setUp(self):
        self.create_url = reverse('create')
        self.register = reverse('account_signup')
        
        self.register1 = {
            'username': 'demo12',
            'password1': 'admin123456',
            'password2': 'admin123456',
            'email': 'admin@mail.com'
        }
        
        self.event2 = Event.objects.create(
            name='Movie',
            place='Central',
            participant=2,
            date=datetime.datetime.today().date(),
            time=(datetime.datetime.today() +
                  datetime.timedelta(hours=1)).time(),

        )
        
        self.register2 = {
            'username': 'demo123',
            'password1': 'admin54343',
            'password2': 'admin54343',
            'email': 'admin1@mail.com'
        }
        

    def test_create_page_response_before_login(self):
        """ create page will redirect you to login"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        # if you are login it will redirect you to create page
        self.assertEqual(response.url, '/accounts/login/?next=/create')

    def test_create_page_response_after_login(self):
        """ create page success response after login"""
        # automatic login after signup
        self.client.post(self.register, self.register1)

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/create_event.html')

    def test_create_event_successful(self):
        """ Test user can create event and then redirect to home"""

        create_event = {
            'name': 'Badminton',
            'place': 'Kaset',
            'participant': 10,
            'joined': 10,
            'date': (datetime.datetime.today() + datetime.timedelta(days=1)).date(),
            'time': (datetime.datetime.today() +
                     datetime.timedelta(hours=1)).time(),
            'create_event': ''
        }
        
        create_event2 = {
            'name': 'Badminton2',
            'place': 'Kaset',
            'participant': 10,
            'joined': 10,
            'date': (datetime.datetime.today() + datetime.timedelta(days=1)).date(),
            'time': (datetime.datetime.today() +
                     datetime.timedelta(hours=1)).time(),
            'create_event': ''
        }

        self.client.post(self.register, self.register1)

        response = self.client.post(self.create_url, create_event)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/all')
        
        # not allow to create same day.
        response = self.client.post(self.create_url, create_event2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/create_event.html')

        # check event that already created
        event = Event.objects.get(id=2)
        self.assertEqual(event.name, 'Badminton')

        # also automatic create HostOfevent model when create event
        host = HostOfEvent.objects.get(id=1)
        self.assertEqual(host.user.username, 'demo12')
        self.assertEqual(host.event.name, 'Badminton')

    def test_do_not_have_name_of_event(self):
        """ If you do not have name of event you can not create event"""
        create_event = {
            'place': 'Kaset',
            'participant': 10,
            'date': (datetime.datetime.today() + datetime.timedelta(days=1)).date(),
            'time': (datetime.datetime.today() +
                     datetime.timedelta(hours=1)).time(),
            'create_event': ''
        }

        self.client.post(self.register, self.register1)

        response = self.client.post(self.create_url, create_event)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/create_event.html')
        self.assertEqual(len(Event.objects.all()), 1)