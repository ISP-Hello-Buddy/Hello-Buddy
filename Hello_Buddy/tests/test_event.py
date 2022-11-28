from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Event, HostOfEvent
import datetime
from django.contrib.auth.models import User

class EventTest(TestCase):
    
    def setUp(self):
        self.create_url = reverse('create')
        self.register = reverse('account_signup')
        self.login = reverse('account_login')
        self.logout = reverse('account_logout')
        
        
        self.user1 = User.objects.create(
            username= 'breeze',
            password= 'demo123456',
            email = 'a@mail.com'
        )
        
        self.user2 = User.objects.create(
            username= 'breeze2',
            password= 'demo123456',
            email = 'b@mail.com'
        )
        
        self.user3 = User.objects.create(
            username= 'breeze3',
            password= 'demo123456',
            email = 'c@mail.com'
        )

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

        self.client.force_login(self.user1)
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
        # self.client.post(self.register, self.register1)
        self.client.force_login(self.user1)
        self.client.post(self.create_url, create_event)
        self.client.logout()
        # login another accout
        self.client.force_login(self.user2)
        
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
        
    def test_join_one_event_per_day(self):
        """ User allow to join one event per day"""
        # create event first
        create_event = {
            'name': 'Badminton',
            'place': 'Kaset',
            'participant': 1,
            'date': (datetime.datetime.today() + datetime.timedelta(days=1)).date(),
            'time': datetime.datetime.today().time(),
            'create_event': ''
        }

        
        # create event
        # self.client.post(self.register, self.register1)
        self.client.force_login(self.user1)
        self.client.post(self.create_url, create_event)
        self.client.logout()
        # login another accout
        self.client.force_login(self.user2)
        self.client.post(self.create_url, create_event)
        self.client.logout()
        
        
        self.client.force_login(self.user3)
        
        event_url = reverse('event', args=[1])
        response = self.client.post(event_url, {'join': ''})
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Event.objects.get(id=1).joined, 1)
        
        event_url1 = reverse('event', args=[2])
        response = self.client.post(event_url1, {'join': ''})
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Event.objects.get(id=2).joined, 0)
        