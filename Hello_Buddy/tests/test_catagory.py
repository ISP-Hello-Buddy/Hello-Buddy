import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



class Test(unittest.TestCase):
        option = webdriver.ChromeOptions()
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

        def login(self):
            """For login"""
            self.browser.get("https://hello-buddy-th.herokuapp.com/home")
            self.browser.find_element(By.LINK_TEXT, "Login").click()
            self.browser.find_element(By.NAME, "login").send_keys(("ForTest"))
            self.browser.find_element(By.NAME, "password").send_keys("admin@1234")
            self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        def test_crate_event(self):
            """test create event"""
            self.login() #login
            # create event
            self.browser.get("https://hello-buddy-th.herokuapp.com/create")
            name = self.browser.find_element(
                By.XPATH, "/html/body/div[2]/form/div[1]/div/div/input")
            place = self.browser.find_element(
                By.XPATH, "/html/body/div[2]/form/div[2]/div/div/input")
            time = self.browser.find_element(
                By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div/input")
            type = self.browser.find_element(By.XPATH, "/html/body/div[2]/form/div[6]/div/div/select")
            name.send_keys("event_test")
            place.send_keys("kaset")
            time.send_keys("23:00:00")
            type.send_keys("eating")

            self.browser.find_element(By.XPATH, "/html/body/div[2]/form/div[8]/button[2]").click()
            self.browser.refresh()
            self.browser.get("https://hello-buddy-th.herokuapp.com/home")
            assert "event_test" in self.browser.page_source

        def test_sort_by_category(self):
            self.browser.get("https://hello-buddy-th.herokuapp.com/eating")
            assert "event_test" in self.browser.page_source
