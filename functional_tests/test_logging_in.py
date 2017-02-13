from .base import FunctionalTest
import time

class RegisterAndLoginTest(FunctionalTest):

    def test_user_can_register(self):
        #User goes to polly site and sees the sign in button
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text("Sign in").click()
        time.sleep(5)

        #A modal pops up with an option to register
        self.browser.find_element_by_link_text("Register").click()

        #He gives his data to register
        self.browser.find_element_by_id("email").send_keys("user@example.com")
        self.browser.find_element_by_id("username").send_keys("User")
        self.browser.find_element_by_id("password").send_keys("password")
        self.browser.find_element_by_id("register").click()

        #After registering his username shows up in the navbar
        self.browser.find_element_by_link_text("User")
