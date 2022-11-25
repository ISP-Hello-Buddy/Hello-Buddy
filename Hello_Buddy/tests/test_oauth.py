from django.test import Client
from Hello_Buddy.views import map
from Hello_Buddy.models import Mapping, Event
from .temp import new_user
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestAuth_E2E(StaticLiveServerTestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test1"
        self.password = "Admin1234@"
        self.user = new_user(self.username, self.password)
        self.user.save()

        self.username2 = "test2"
        self.password2 = "Tester2@"
        self.user2 = new_user(self.username2, self.password2)
        self.user.save()

        self.event = Event.objects.create(
            name="event", place="มหาลัยเกษตร", participant=4, joined=1, date="2022-11-22", type="", image_upload="event/images/default.jpg", time="14:52:48")
        self.map = Mapping.objects.create(address="เกษตร",
                                          lon=1, lat=1, event=self.event, user=self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = ChromeOptions()
        options.add_argument("--headless")
        cls.browser = Chrome(options=options)
        # cls.browser.get(cls.live_server_url)

    # @override_settings(DEBUG=True)
    def login(self):
        self.client.login(username=self.username, password=self.password)
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

    def test_login(self):
        """check login function in web form """
        self.browser.get(self.live_server_url)
        but_login = self.browser.find_element(By.XPATH , "/html/body/nav/div/ul[2]/li[2]/a")
        but_login.click()
        # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
        username = self.browser.find_element(By.ID,"id_login")
        password = self.browser.find_element(By.ID,"id_password")
        submit = self.browser.find_element(By.XPATH , "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
        #send data input
        time.sleep(1)
        username.send_keys(self.username2)
        password.send_keys(self.password2)
        submit.send_keys(Keys.RETURN)

        # submit form
        assert "test2" in self.browser.page_source

    def test_wrong_login(self):
        """Check login in function detect wrong user"""
        self.browser.get(self.live_server_url)
        but_login = self.browser.find_element(By.XPATH , "/html/body/nav/div/ul[2]/li[2]/a")
        but_login.click()
        username = self.browser.find_element(By.ID,"id_login")
        password = self.browser.find_element(By.ID,"id_password")
        submit = self.browser.find_element(By.XPATH , "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
        #send data input
        username.send_keys(self.username2)
        password.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

        time.sleep(1)
        assert "The username and/or password you specified are not correct." in self.browser.page_source
        self.browser.get(self.live_server_url)

    def test_logout(self):
        """Check logout function this website"""
        self.browser.get(self.live_server_url)
        self.login()
        time.sleep(1)
        logout = self.browser.find_element(By.XPATH , "/html/body/nav/div/ul[2]/li[2]/a")
        assert " Logout" in self.browser.page_source
        logout.click()
        conf_out = self.browser.find_element(By.XPATH , "/html/body/nav/div/div[2]/form/div/div/button[1]")
        conf_out.click()
        assert " Login" in self.browser.page_source


    def test_come_google_login(self):
        self.browser.get("https://hello-buddy-th.herokuapp.com/home")
        time.sleep(1)
        but_login = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[2]/li[2]/a")
        but_login.click()
        time.sleep(1)
        but_google = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[9]/p/a[1]")
        but_google.click()
        con_ = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/form/button")
        con_.click()
        
        txt = self.browser.current_url# html = '<svg xmlns="https://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 48 48" aria-hidden="true" class="L5wZDc"><path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"></path><path fill="#34A853" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z"></path><path fill="#FBBC05" d="M11.69 28.18C11.25 26.86 11 25.45 11 24s.25-2.86.69-4.18v-5.7H4.34C2.85 17.09 2 20.45 2 24c0 3.55.85 6.91 2.34 9.88l7.35-5.7z"></path><path fill="#EA4335" d="M24 10.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 4.18 29.93 2 24 2 15.4 2 7.96 6.93 4.34 14.12l7.35 5.7c1.73-5.2 6.58-9.07 12.31-9.07z"></path><path fill="none" d="M2 2h44v44H2z"></path></svg>'
        x = txt.split("/")
        assert "accounts.google.com" in x

    def test_come_github_login(self):
        self.browser.get("https://hello-buddy-th.herokuapp.com/home")
        time.sleep(1)
        but_login = self.browser.find_element(
            By.XPATH, "/html/body/nav/div/ul[2]/li[2]/a")
        but_login.click()
        time.sleep(1)
        but_github = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[9]/p/a[2]")
        but_github.click()
        con_ = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/form/button")
        con_.click()
        
        txt = self.browser.current_url
        x = txt.split("/")
        assert "github.com" in x
    
    
    def test_register(self):
        """check login function in web form """
        self.browser.get(self.live_server_url)
        but_regis = self.browser.find_element(By.XPATH , "/html/body/nav/div/ul[2]/li[1]/a")
        but_regis.click()
        # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
        username = self.browser.find_element(By.ID,"id_username")
        email = self.browser.find_element(By.ID,"id_email")
        password1 = self.browser.find_element(By.XPATH,"/html/body/div/div[2]/div/div/form/div/div[2]/div[6]/input")
        password2= self.browser.find_element(By.XPATH,"/html/body/div/div[2]/div/div/form/div/div[2]/div[8]/input")

        submit = self.browser.find_element(By.XPATH , "/html/body/div/div[2]/div/div/form/div/div[2]/div[10]/button")
        #send data input
        time.sleep(1)
        username.send_keys("rew_inwza")
        email.send_keys("rew_inwza@gmail.com")
        password1.send_keys("Admin1234@")
        password2.send_keys("Admin1234@")
        submit.send_keys(Keys.RETURN)

        # submit form
        assert "rew_inwza" in self.browser.page_source










