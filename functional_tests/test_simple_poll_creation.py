from .base import FunctionalTest
import time

class NewPollTest(FunctionalTest):

    def test_user_can_create_new_poll(self):

        #User hears about Polly, goes to check it out
        self.browser.get('http://localhost:8000')
        title=self.browser.find_element_by_css_selector('.title').text
        self.assertEqual(title, 'Polly')

        #Sees create new poll button on the home webpage
        self.browser.find_element_by_link_text('New poll').click()

        #Creates a new poll
        self.browser.find_element_by_id('id_question_text').send_keys('How many?')
        self.browser.find_element_by_id('id_Option1').send_keys('41')
        self.browser.find_element_by_id('id_Option2').send_keys('42\n')

        #After submitting the poll, the page redirects to the polls page.
        title=self.browser.find_element_by_css_selector('.title').text
        self.assertEqual(title, 'Polls')
        #Here the User can see a link to his poll.
        self.browser.find_element_by_link_text('How many?')
