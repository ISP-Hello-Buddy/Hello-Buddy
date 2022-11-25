from django.test import Client
from Hello_Buddy.views import map
from Hello_Buddy.models import Mapping, Event
from .temp import new_user
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestCatagory(StaticLiveServerTestCase):

    def setUp(self):
        self.non_type_event = Event.objects.create(
            name="event1", place="มหาลัยเกษตร",
            participant=1, joined=1, date="2022-11-22",
            type="", image_upload="event/images/default.jpg",
            time="10:52:48")

        self.eating_event = Event.objects.create(
            name="Eating", place="มหาลัยเกษตร",
            participant=4, joined=0, date="2022-11-22",
            type="", image_upload="event/images/default.jpg",
            time="00:52:48")

        self.party_event = Event.objects.create(
            name="Party", place="มหาลัยเกษตร",
            participant=6, joined=1, date="2022-11-22",
            type="", image_upload="event/images/default.jpg",
            time="00:52:48")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = ChromeOptions()
        options.add_argument("--headless")
        cls.browser = Chrome(options=options)