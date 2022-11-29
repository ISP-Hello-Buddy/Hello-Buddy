import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class TestProfilePage(unittest.TestCase):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def test_login(self):
        self.browser.get("https://hello-buddy-th.herokuapp.com")
        self.browser.find_element(By.LINK_TEXT, "Login").click()
        self.browser.find_element(By.NAME, "login").send_keys("teste2e")
        self.browser.find_element(By.NAME, "password").send_keys("kl;'1234")
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

    def test_change_information(self):
        self.browser.get("https://hello-buddy-th.herokuapp.com")
        self.browser.find_element(By.LINK_TEXT, "Login").click()
        self.browser.find_element(By.NAME, "login").send_keys("teste2e")
        self.browser.find_element(By.NAME, "password").send_keys("kl;'1234")
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        profile_path = "/profile-user"
        self.browser.get("https://hello-buddy-th.herokuapp.com"+profile_path)
        self.browser.find_element(By.NAME, "username").clear()
        self.browser.find_element(By.NAME, "username").send_keys("new_username")
        self.browser.find_element(By.NAME, "email").clear()
        self.browser.find_element(By.NAME, "email").send_keys("new_email@hotmail.com")
        self.browser.find_element(By.NAME, "bio").clear()
        self.browser.find_element(By.NAME, "bio").send_keys("hi there")
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
        username = self.browser.find_element(By.NAME, "username").get_attribute("value")
        email = self.browser.find_element(By.NAME, "email").get_attribute("value")
        bio = self.browser.find_element(By.NAME, "bio").get_attribute("value")
        self.assertEqual(username, "new_username")
        self.assertEqual(email, "new_email@hotmail.com")
        self.assertEqual(bio, "hi there")

    def test_clickable(self):
        self.browser.get("https://hello-buddy-th.herokuapp.com")
        self.browser.find_element(By.LINK_TEXT, "Login").click()
        self.browser.find_element(By.NAME, "login").send_keys("teste2e")
        self.browser.find_element(By.NAME, "password").send_keys("kl;'1234")
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        profile_path = "/profile-user"
        self.browser.get("https://hello-buddy-th.herokuapp.com"+profile_path)
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').is_enabled()