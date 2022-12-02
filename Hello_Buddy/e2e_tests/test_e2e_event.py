import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
from decouple import config



class TestCreateEvent(unittest.TestCase):

    def setUp(self):
        self.url = config('URL', default="http://127.0.0.1:8000/home")
        self.register1 = {
            'username': config('USERNAME', default='YOUR-USERNAME'),
            'password1': config('PASS1', default='YOUR-PASSWORD'),
            'password2': config('PASS2', default='YOUR-PASSWORD-AGAIN'),
            'email': config('EMAIL', default='YOUR-EMAIL'),
        }
        # options = ChromeOptions()
        # options.add_argument("--headless")
        self.browser = webdriver.Chrome()

    def register(self):
        self.browser.get(self.url)

        login = self.browser.find_elements(By.PARTIAL_LINK_TEXT, 'Sign Up')
        login[0].click()

        username = self.browser.find_elements(By.NAME, 'username')
        username[0].send_keys(self.register1['username'])
        password1 = self.browser.find_elements(By.NAME, 'password1')
        password1[0].send_keys(self.register1['password1'])
        password2 = self.browser.find_elements(By.NAME, 'password2')
        password2[0].send_keys(self.register1['password2'])
        email = self.browser.find_elements(By.NAME, 'email')
        email[0].send_keys(self.register1['email'])
        sign_in = self.browser.find_elements(By.TAG_NAME, 'button')
        sign_in[0].click()
        time.sleep(3)

    def login(self):

        login = self.browser.find_elements(By.PARTIAL_LINK_TEXT, 'Login')
        login[0].click()

        username = self.browser.find_elements(By.NAME, 'login')
        username[0].send_keys(self.register1['username'])
        password = self.browser.find_elements(By.NAME, 'password')
        password[0].send_keys(self.register1['password1'])
        signin = self.browser.find_elements(By.TAG_NAME, 'button')
        signin[0].click()

    def test_create_event(self):
        self.register()
        time.sleep(3)

        create = self.browser.find_elements(By.PARTIAL_LINK_TEXT, 'Create')
        create[0].click()

        name = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
        place = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
        time_ = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")


        name.send_keys("e2e_test1")
        place.send_keys("kaset")
        time_.send_keys("01:00:00")
        sub = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form/div[8]/button[2]")
        sub.click()


        assert "e2e_test1" in self.browser.page_source

    def test_create_event_wrong_place_submit(self):
        self.browser.get(self.url)
        self.login()
        time.sleep(3)

        but_create = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[1]/li[4]/a")
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
        self.browser.get(self.url)
        self.login()
        time.sleep(3)

        but_create = self.browser.find_element(
            By.XPATH, "/html/body/header/nav/div/ul[1]/li[4]/a")
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


    if __name__ == "__main__":
        unittest.main()
