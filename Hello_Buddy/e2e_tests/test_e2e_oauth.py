from django.test import Client
from Hello_Buddy.views import map
from Hello_Buddy.models import Mapping, Event
from .temp import new_user
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import namegenerator
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
class TestAuth_E2E(StaticLiveServerTestCase):

    def setUp(self):
        
        self.client = Client()
        self.name_regis = namegenerator.gen()
        
    
        self.username = namegenerator.gen()
        self.password = "Admin1234@"
        self.user = new_user(self.username, self.password)
        self.user.save()

        self.username2 = namegenerator.gen()
        self.password2 = "Tester2@"
        self.user2 = new_user(self.username2, self.password2)
        
        self.username_new = namegenerator.gen()
        self.password_new = "Admin1234@"
        self.email_new = "test@test.com"
          
        self.username_new2 = namegenerator.gen()
        self.password_new2 = "Admin1234@"
        self.email_new2 = "test@test.com"
        # self.user2 = new_user(self.username2, self.password2)
        self.user.save()

        self.event = Event.objects.create(
            name="event", place="มหาลัยเกษตร", participant=4, joined=1, date="2022-11-22", type="", image_upload="event/images/default.jpg", time="14:52:48")
        self.map = Mapping.objects.create(address="เกษตร",
                                          lon=1, lat=1, event=self.event, user=self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = ChromeOptions()
        # options.add_argument("--headless")
        cls.browser = Chrome(options=options)
        cls.my_web = cls.live_server_url
        # cls.my_web = "https://hello-buddy-th.herokuapp.com/home"
        # cls.browser.set_window_size(1920, 1080)
    
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
        self.browser.get(self.my_web)
        but_login = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
        but_login.click()
        # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
        username = self.browser.find_element(By.ID, "id_login")
        password = self.browser.find_element(By.ID, "id_password")
        submit = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
        # send data input
        time.sleep(1)
        username.send_keys(self.username2)
        password.send_keys(self.password2)
        submit.send_keys(Keys.RETURN)

        # submit form
        assert self.username2 in self.browser.page_source

    def test_wrong_login(self):
        """Check login in function detect wrong user"""
        self.browser.get(self.my_web)
        but_login = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]/a")
        but_login.click()
        username = self.browser.find_element(By.ID, "id_login")
        password = self.browser.find_element(By.ID, "id_password")
        submit = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
        # send data input
        username.send_keys(self.username2)
        password.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

        time.sleep(1)
        assert "The username and/or password you specified are not correct." in self.browser.page_source
        # self.browser.get(self.live_server_url)
    
    def test_register(self):
        """check login function in web form """
        
        self.browser.get(self.my_web)
        but_regis = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[2]/li[1]")
        but_regis.click()
        # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
        username = self.browser.find_element(By.ID, "id_username")
        email = self.browser.find_element(By.ID, "id_email")
        password1 = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[6]/input")
        password2 = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[8]/input")

        submit = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[10]/button")
        # send data input
        time.sleep(1)
        username.send_keys(self.username_new)
        email.send_keys(self.email_new)
        password1.send_keys(self.password_new)
        password2.send_keys(self.password_new)
        submit.send_keys(Keys.RETURN)

        # submit form
        assert self.username_new in self.browser.page_source
        
    def test_user_account_is_used(self):
        """check login function in web form in_main_server """
        self.browser.get(self.my_web)
        but_regis = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[2]/li[1]")
        but_regis.click()
        
        # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
        username = self.browser.find_element(By.ID, "id_username")
        email = self.browser.find_element(By.ID, "id_email")
        password1 = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[6]/input")
        password2 = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[8]/input")

        submit = self.browser.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[10]/button")
        # send data input
        time.sleep(1)
        username.send_keys(self.username_new)
        email.send_keys(self.email_new)
        password1.send_keys("Admin1234@")
        password2.send_keys("Admin1234@")
        submit.send_keys(Keys.RETURN)

        # submit form
        assert self.username_new in self.browser.page_source
        
    # def test_logout(self):
    #     """Check logout function this website"""
    #     name =  namegenerator.gen()
    #     password_ = "Admin1234@"
    #     x =namegenerator.gen() 
    #     email_key =   str(x) + "@gmail.com"
        
    #     # self.browser.get(self.my_web)
    #     self.browser.get(self.live_server_url)
    #     but_regis = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[1]")
    #     but_regis.click()
        
    #     # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
    #     username = self.browser.find_element(By.ID, "id_username")
    #     email = self.browser.find_element(By.ID, "id_email")
    #     password1 = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[6]/input")
    #     password2 = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[8]/input")

    #     submit = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[10]/button")

    #     # send data input
    #     time.sleep(1)
    #     username.send_keys(name)
    #     email.send_keys(email_key)
    #     password1.send_keys(self.password_new2)
    #     password2.send_keys(self.password_new2)
    #     submit.send_keys(Keys.RETURN)
    #     # register completion
    #     but_out = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_out.click()
        
    #     time.sleep(2)
        
    #     assert " Logout" in self.browser.page_source 
        
    #     # self.client.logout()
    #     # self.browser.refresh()
    #     time.sleep(2)
    #     re = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]/a")
    #     self.browser.execute_script("arguments[0].click();", re)
    #     # self.browser.execute_script("arguments[0].removeAttribute('style')", re)  
    #     # self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, 20).until(
    #     #     EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-large' and @id='sprawdz']"))))
    #     # self.client.logout()
    #     # re.click()
    
    #     re.click()
    
    
    # def test_come_google_login(self):
    #     self.browser.get("https://hello-buddy-th.herokuapp.com/home")
    #     time.sleep(1)
    #     but_login = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_login.click()
    #     time.sleep(1)
    #     but_google = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[9]/p/a[1]")
    #     but_google.click()
    #     con_ = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/form/button")
    #     con_.click()

    #     txt = self.browser.current_url
    #     x = txt.split("/")
    #     assert "accounts.google.com" in x

    # def test_come_github_login(self):
    #     web_ = "https://hello-buddy-th.herokuapp.com/home"
        
    #     self.browser.get(self.live_server_url)
    #     time.sleep(1)
    #     but_login = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_login.click()
    #     time.sleep(1)
    #     but_github = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[9]/p/a[2]")
    #     but_github.click()
    #     con_ = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/form/button")
    #     con_.click()

    #     txt = self.browser.current_url
    #     x = txt.split("/")
    #     assert "github.com" in x

    # def test_login_in_main_server(self):
    #     """check login function in web form in main server"""
    #     self.browser.get("https://hello-buddy-th.herokuapp.com/home")
    #     but_login = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_login.click()
    #     # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
    #     username = self.browser.find_element(By.ID, "id_login")
    #     password = self.browser.find_element(By.ID, "id_password")
    #     submit = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
    #     # send data input
    #     time.sleep(1)
    #     username.send_keys(self.username2)
    #     password.send_keys(self.password2)
    #     submit.send_keys(Keys.RETURN)

    #     # submit form
    #     assert "test2" in self.browser.page_source

    # def test_wrong_login_in_main_server(self):
    #     """Check login in function detect wrong user in main server"""
    #     self.browser.get("https://hello-buddy-th.herokuapp.com/home")
    #     but_login = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_login.click()
    #     username = self.browser.find_element(By.ID, "id_login")
    #     password = self.browser.find_element(By.ID, "id_password")
    #     submit = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
    #     # send data input
    #     username.send_keys(self.username2)
    #     password.send_keys(self.password)
    #     submit.send_keys(Keys.RETURN)

    #     time.sleep(1)
    #     assert "The username and/or password you specified are not correct." in self.browser.page_source
    #     # self.browser.get(self.live_server_url)

    # def test_logout_in_main_server(self):
    #     """Check logout function this website in main server"""
    #     self.browser.get(self.live_server_url)
    #     but_login = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]")
    #     but_login.click()
    #     # assert "DON'T HAVE AN ACCOUNT?" in self.browser.page_source
    #     username = self.browser.find_element(By.ID, "id_login")
    #     password = self.browser.find_element(By.ID, "id_password")
    #     submit = self.browser.find_element(
    #         By.XPATH, "/html/body/div/div[2]/div/div/form/div/div[2]/div[7]/button")
    #     # send data input
    #     time.sleep(1)
    #     username.send_keys("test_e2e_web001")
    #     password.send_keys("Admin1234@")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(5)
    #     logout = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/ul[2]/li[2]/a")
    #     assert " Logout" in self.browser.page_source
    #     logout.click()
    #     conf_out = self.browser.find_element(
    #         By.XPATH, "/html/body/header/nav/div/div[2]/form/div/div/button[1]")
    #     conf_out.click()
    #     assert " Login" in self.browser.page_source