from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Event, HostOfEvent
import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestCatagory(TestCase):

    def setUp(self):
        self.create_url = reverse('create')
        self.register = reverse('account_signup')

        self.account1 = {
            'username': 'demo12',
            'password1': 'admin123456',
            'password2': 'admin123456',
            'email': 'admin@mail.com'
        }

    def revers_toevent_catagory(self, type:str):
        return reverse(type)

    def test_revers_to_catagory(self):
        self.client.post(self.register, self.account1)

        eating_event = Event.objects.create(
            name="Eating", place="มหาลัยเกษตร",
            participant=4, joined=0, date="2022-11-22",
            type="", image_upload="event/images/default.jpg",
            time="00:52:48")

        response = self.client.post(self.create_url, )
        self.assertEqual(response.status_code, 302)




        # self.non_type_event = Event.objects.create(
        #     name="event1", place="มหาลัยเกษตร",
        #     participant=1, joined=1, date="2022-11-22",
        #     type="", image_upload="event/images/default.jpg",
        #     time="10:52:48")
        #
        #
        # self.party_event = Event.objects.create(
        #     name="Party", place="มหาลัยเกษตร",
        #     participant=6, joined=1, date="2022-11-22",
        #     type="", image_upload="event/images/default.jpg",
        #     time="00:52:48")


