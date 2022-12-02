from django.test import TestCase, Client
from django.urls import reverse, resolve
from Hello_Buddy.views import  map
from Hello_Buddy.models import Mapping, Event 
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# from .until import new_user
# from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.common.by import By
# import time
UserModel = get_user_model()

class TestMap(TestCase):
    def setUp(self):
        self.client = Client()
        self.map_url = reverse("map")
        self.user = UserModel.objects.create_user(
            "test_user", "test@example.com", "admin1234")
        self.event = Event.objects.create(
            name="event", place="มหาลัยเกษตร", participant=4, joined=1, date="2022-11-22", type="", image_upload="",time = "14:52:48")
        self.event_2 = Event.objects.create(
            name="event_2", place="ประเทศไทย", participant=7, joined=2, date="2021-10-21", type="", image_upload="",time = "14:52:48")
        self.event_3 = Event.objects.create(
            name="event_3", place="เกษตร", participant=7, joined=2, date="2020-9-21", type="", image_upload="",time ="14:52:48")
        
    def test_map_url_is_resolved(self):
        """test url resolve of map from url_patterm"""
        url = self.map_url
        self.assertEqual(resolve(url).func, map)

    def test_model_map_full_name_location(self):
        """test name location address when use full name loacation"""
        loca = "สามย่าน, สะพานไทย - ญี่ปุ่น, แขวงปทุมวัน, เขตปทุมวัน, กรุงเทพมหานคร, 10330, ประเทศไทย"
        mp = Mapping.objects.create(address=loca,
                                    lon=1, lat=1, event=self.event, user=self.user)
        map_loca = str(mp)
        check_loca = "สามย่าน, สะพานไทย - ญี่ปุ่น, แขวงปทุมวัน, เขตปทุมวัน, กรุงเทพมหานคร, 10330, ประเทศไทย"
        self.assertEqual(map_loca, check_loca)

    def test_model_map_small_text_location(self):
        """test map loction when use low text location name"""
        loca = "อารีย์"
        mp = Mapping.objects.create(address=loca,
                                    lon=1, lat=1, event=self.event, user=self.user)
        map_loca = str(mp)
        check_loca = "อารีย์, ถนนพหลโยธิน, สะพานควาย, แขวงพญาไท, เขตพญาไท, กรุงเทพมหานคร, 10400, ประเทศไทย"
        self.assertEqual(map_loca, check_loca)

    def test_model_map_not_found_location(self):
        """test map loction when this location not have in map"""
        loca = "SKE19 ISP LOVE YOU"
        mp = Mapping.objects.create(address=loca,
                                    lon=1, lat=1, event=self.event, user=self.user)
        map_loca = str(mp)
        text_get = "Not_location"
        self.assertEqual(map_loca, text_get)

    def test_delete_event_and_map(self):
        """test deleting event then map of events is delete"""
        Mapping.objects.create(address="dekub",
                                    lon=1, lat=1, event=self.event, user=self.user)
        num_map_before = len(Mapping.objects.all())
        self.assertEqual(num_map_before, 1)
        pk = self.event.pk
        get_event_out = Event.objects.get(pk=pk)
        get_event_out.delete()
        Mapping.objects.all()
        num_map_after = len(Mapping.objects.all())
        self.assertEqual(num_map_after, 0)

    def test_delete_event_one_and_more_map(self):
        """Test deleting events. Then the event map is also deleted"""
        Mapping.objects.create(address="address_test1",
                                     lon=1, lat=1, event=self.event, user=self.user)
        Mapping.objects.create(address="address_test2",
                                     lon=1, lat=1, event=self.event, user=self.user)
        Mapping.objects.create(address="address_test3",
                                     lon=1, lat=1, event=self.event, user=self.user)
        num_map_before = len(Mapping.objects.all())
        self.assertEqual(num_map_before, 3)
        pk = self.event.pk
        get_event_out = Event.objects.get(pk=pk)
        get_event_out.delete()
        Mapping.objects.all()
        num_map_after = len(Mapping.objects.all())
        self.assertEqual(num_map_after, 0)

    def test_delete_one_by_one_map_event(self):
        """test a lot of deleting event then map of events are deleted"""
        Mapping.objects.create(address="address_test1",
                                     lon=1, lat=1, event=self.event, user=self.user)
        Mapping.objects.create(address="address_test2",
                                     lon=1, lat=1, event=self.event_2, user=self.user)
        Mapping.objects.create(address="address_test3",
                                     lon=1, lat=1, event=self.event_3, user=self.user)
        Mapping.objects.create(address="address_test4",
                                     lon=1, lat=1, event=self.event_2, user=self.user)
        num_map_before = len(Mapping.objects.all())
        self.assertEqual(num_map_before, 4)
        pk = self.event.pk
        get_event_out = Event.objects.get(pk=pk)
        get_event_out.delete()
        Mapping.objects.all()
        num_map_after = len(Mapping.objects.all())
        self.assertEqual(num_map_after, 3)
        pk = self.event_2.pk
        get_event_out = Event.objects.get(pk=pk)
        get_event_out.delete()
        Mapping.objects.all()
        num_map_after_final = len(Mapping.objects.all())
        self.assertEqual(num_map_after_final, 1)

    def test_delete_user_and_map(self):
        """test deleting user then map of user it will not deleted"""
        Mapping.objects.create(address="address_test1",
                                     lon=1, lat=1, event=self.event, user=self.user)
        Mapping.objects.create(address="address_test2",
                                     lon=1, lat=1, event=self.event, user=self.user)
        Mapping.objects.create(address="address_test3",
                                     lon=1, lat=1, event=self.event, user=self.user)
        num_map_before = len(Mapping.objects.all())
        self.assertEqual(num_map_before, 3)
        pk = self.user.pk
        get_user_out = UserModel.objects.get(pk=pk)
        get_user_out.delete()
        Mapping.objects.all()
        num_map_after = len(Mapping.objects.all())
        self.assertEqual(num_map_after,3)