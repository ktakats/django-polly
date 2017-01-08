from django.test import TestCase

from polly.forms import newPollForm

class NewPollFormTest(TestCase):

    def test_form_has_placeholder(self):
        form=newPollForm()
        self.assertIn('placeholder="Your question"', form.as_p())
        self.assertIn('placeholder="Option 1"', form.as_p())
        self.assertIn('placeholder="Option 2"', form.as_p())

    
