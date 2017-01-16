from django.test import TestCase
from polls.models import Question, Options
from polly.forms import newPollForm
from django.contrib.auth.models import User

class NewPollFormTest(TestCase):

    def test_form_has_placeholder(self):
        form=newPollForm()
        self.assertIn('placeholder="Your question"', form.as_p())
        self.assertIn('placeholder="Option 1"', form.as_p())
        self.assertIn('placeholder="Option 2"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form=newPollForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['question_text'], ['You can not have an empty poll question'])

    def test_form_save_function(self):
        user=User.objects.create()
        form=newPollForm(data={'question_text': 'Bla', 'option_0': 'zero', 'option_1': 'one', 'option_count': '2'})
        self.assertTrue(form.is_valid())
        new_question=form.save(user)
        self.assertEqual(new_question, Question.objects.first())

    def test_form_can_have_more_than_two_options(self):
        user=User.objects.create()
        form=newPollForm(data={'question_text': 'Bla', 'option_0': 'zero', 'option_1': 'one', 'option_2': 'two', 'option_count': '3'})
        self.assertTrue(form.is_valid())
        new_question=form.save(user)
        self.assertEqual(new_question, Question.objects.first())
        self.assertIn('two', Options.objects.all())
