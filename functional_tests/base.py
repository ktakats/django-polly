from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()
