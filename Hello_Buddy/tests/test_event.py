from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Event
import datetime

class EventTest(TestCase):
    
    def setUp(self):
        self.create_url = reverse('create')
        self.register = reverse('account_signup')
        self.login = reverse('account_login')
        self.logout = reverse('account_logout')
        
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

    def test_event_page_response_before_login(self):
        """ event page will redirect you to login"""
        event_url = reverse('event', args=[1])
        response = self.client.get(event_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/event/1')

    def test_event_page_response_after_login(self):
        """ event page succesful response after login"""
        
        # create event first
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

        self.client.post(self.register, self.register1)
        self.client.post(self.create_url, create_event)

        # go to see on event page
        event_url = reverse('event', args=[1])
        response = self.client.get(event_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Hello_Buddy/event.html')
        
    def test_join_and_cancel_event(self):
        """ Test user join the event"""
        
        # create event first
        create_event = {
            'name': 'Badminton',
            'place': 'Kaset',
            'participant': 1,
            'date': (datetime.datetime.today() + datetime.timedelta(days=1)).date(),
            'time': (datetime.datetime.today() +
                     datetime.timedelta(hours=1)).time(),
            'create_event': ''
        }

        # create event
        self.client.post(self.register, self.register1)
        self.client.post(self.create_url, create_event)
        self.client.post(self.logout)
        # login another accout
        self.client.post(self.register, self.register2)
        
        event_url = reverse('event', args=[1])
        # check participant before join
        self.assertEqual(Event.objects.get(id=1).joined, 0)
        # join the event
        response = self.client.post(event_url, {'join': ''})
        self.assertEqual(response.status_code, 200)
        # check participant after join
        self.assertEqual(Event.objects.get(id=1).joined, 1)
        self.assertTemplateUsed(response, 'Hello_Buddy/event.html')
        
        # check participant after cancel
        response = self.client.post(event_url, {'cancel': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.get(id=1).joined, 0)
        self.assertTemplateUsed(response, 'Hello_Buddy/event.html')
        