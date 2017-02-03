from .base import FunctionalTest
import time
from django.contrib.auth.models import User
from unittest import skip


class PollTest(FunctionalTest):

#  @skip("strange")
  def test_user_can_vote_in_a_poll(self):
      #User goes to Polly and creates a new poll
      user=User.objects.create(username='admin', email="bla@example.com", password='password')
      self.browser.get(self.live_server_url)
      self.browser.find_element_by_link_text('New poll').click()
      self.browser.find_element_by_id('id_question_text').send_keys('How many?')
      self.browser.find_element_by_id('id_form-0-option_text').send_keys('40')
      self.browser.find_element_by_id('id_form-1-option_text').send_keys('42\n')

      ##He decides to cast his own vote at the poll, so on the polls page clicks on the poll
      self.browser.find_element_by_link_text('How many?').click()

      #Here he can see the two original options
      bla=self.browser.find_element_by_tag_name('body').text
      self.assertIn('40', bla)
      self.assertIn('42', bla)

      #He decides to vote for 42
      self.browser.find_element_by_css_selector('#id_option_text_1').click()
      self.browser.find_element_by_css_selector('.btn-default').click()
      self.browser.find_element_by_id('resultplot')


      #After submitting his vote, he can see a plot showing the results of the poll

      #He can also add more options to the poll
