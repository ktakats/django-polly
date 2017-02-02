from .base import FunctionalTest
import time
from django.contrib.auth.models import User

class NewPollTest(FunctionalTest):

    def test_user_can_create_new_poll(self):

        #User hears about Polly, goes to check it out
        user=User.objects.create(username='admin', email="bla@example.com", password='password')
        self.browser.get(self.live_server_url)
        title=self.browser.find_element_by_css_selector('.title').text
        self.assertEqual(title, 'Polly')

        #Sees create new poll button on the home webpage
        self.browser.find_element_by_link_text('New poll').click()

        #Creates a new poll
        self.browser.find_element_by_id('id_question_text').send_keys('How many?')
        self.browser.find_element_by_id('id_form-0-option_text').send_keys('40')
        self.browser.find_element_by_id('id_form-1-option_text').send_keys('42')
        self.browser.find_element_by_css_selector(".add-row").click()
        self.browser.find_element_by_name('form-2-option_text').send_keys('0\n')

        #After submitting the poll, the page redirects to the polls page.
        title=self.browser.find_element_by_css_selector('.title').text
        self.assertEqual(title, 'Polls')
