from django.test import Client
from Hello_Buddy.views import map
from Hello_Buddy.models import Mapping, Event
from .temp import new_user
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import resolve


class TestCreateEvent(StaticLiveServerTestCase):

    def setUp(self):
        self.client = Client()
        self.username1 = "testuser"
        self.password1 = "test123456"
        self.user = new_user(self.username1, self.password1)
        self.user.save()

        self.username2 = "test2"
        self.password2 = "Tester2@"
        self.user2 = new_user(self.username2, self.password2)
        self.user.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # options = ChromeOptions()
        # options.add_argument("--headless")
        cls.browser = Chrome()
        # cls.browser.get(cls.live_server_url)

    def login_id1(self):
        self.client.login(username=self.username1, password=self.password1)
        cookie = self.client.cookies["sessionid"]
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "path": "/",
            }
        )
        self.browser.refresh()

    def login_id2(self):
        self.client.login(username=self.username2, password=self.password2)
        cookie = self.client.cookies["sessionid"]
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "path": "/",
            }
        )
        self.browser.refresh()

    def test_redirect_create_event_page(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        assert "Image upload" in self.browser.page_source

    def test_not_login_create_event(self):
        self.browser.get(self.live_server_url)
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        assert "Image upload" not in self.browser.page_source

    def test_create_event(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")

        name.send_keys("e2e_test1")
        place.send_keys("kaset")
        time.send_keys("01:00:00")

        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[2]")
        sub.click()

        self.browser.refresh()

        assert "e2e_test1" in self.browser.page_source

    def test_create_event_wrong_place_submit(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time_ = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")

        name.send_keys("e2e_test1")
        place.send_keys("I love ISP and Jame ")
        time_.send_keys("01:00:00")

        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[2]")
        sub.click()
        time.sleep(1)

        assert "This location has not on the map location" in self.browser.page_source

    def test_create_event_wrong_place_check_place(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time_ = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")

        name.send_keys("e2e_test1")
        place.send_keys("I love ISP and Jame ")
        time_.send_keys("01:00:00")

        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[1]")
        sub.click()
        time.sleep(1)

        assert "Location is None" in self.browser.page_source

    def test_in_to_event_created(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time_ = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")

        name.send_keys("e2e_test2")
        place.send_keys("karset")
        time_.send_keys("01:00:00")

        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[2]")
        sub.click()

        time.sleep(2)
        assert "e2e_test2" in self.browser.page_source

        event_ = self.browser.find_element(
            By.XPATH, "/html/body/div/div/div/a/div/div/img")
        event_.click()

        time.sleep(2)

        assert "YOU ARE THE OWNER" in self.browser.page_source

    def test_join_event_another_user(self):
        self.browser.get(self.live_server_url)

        self.login_id1()
        but_create = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[1]/li[4]/a")
        but_create.click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time_ = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")

        name.send_keys("e2e_test3")
        place.send_keys("karset")
        time_.send_keys("01:00:00")

        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[2]")
        sub.click()
        time.sleep(1)

        self.login_id2()
        time.sleep(1)

        event_page = self.browser.find_element(
            By.XPATH, "/html/body/div/div/div/a/div/div/img")
        event_page.click()
        time.sleep(1)
        assert "Participant: 0/1" in self.browser.page_source

        join_ = self.browser.find_element(
            By.XPATH, "/html/body/div/div/div/div[2]/div/form/button")
        join_.click()
        assert "Participant: 1/1" in self.browser.page_source
