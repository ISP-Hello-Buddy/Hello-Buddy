from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class TestCreateEvent(StaticLiveServerTestCase):
    
    def setUp(self) :
        self.browser = webdriver.Chrome()
    
    def setUplogin(self):
        self.browser.get(self.live_server_url)
        User.objects.create_user(username='testuser', password='test123456')
        
        login = self.browser.find_elements(By.PARTIAL_LINK_TEXT, 'Create')
        login[0].click()
        
        username = self.browser.find_elements(By.NAME, 'login')
        username[0].send_keys('testuser')
        password = self.browser.find_elements(By.NAME, 'password')
        password[0].send_keys('test123456')
        signin = self.browser.find_elements(By.TAG_NAME, 'button')
        signin[0].click()
        
    def test_create_event(self):
        self.setUplogin()
        

        