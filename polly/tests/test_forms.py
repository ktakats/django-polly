from django.test import TestCase
from polls.models import Question, Options
from polly.forms import newPollForm, OptionForm
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory

class NewPollFormTest(TestCase):

    def test_form_has_placeholder(self):
        form=newPollForm()
        self.assertIn('placeholder="Your question"', form.as_p())
    #    self.assertIn('placeholder="Option 1"', form.as_p())
    #    self.assertIn('placeholder="Option 2"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form=newPollForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['question_text'], ['You can not have an empty poll question'])

    def test_form_save_function(self):
        OptionFormSet=formset_factory(OptionForm, extra=2)
        user=User.objects.create()
        form=newPollForm(data={'question_text': 'test'})
        formset=OptionFormSet(data={'form-1-option_text': 'one', 'form-0-option_text': 'zero',  'form-MAX_NUM_FORMS': '1000', 'form-TOTAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-INITIAL_FORMS': '0'})
        self.assertTrue(form.is_valid())
        self.assertTrue(formset.is_valid())
        new_question=form.save(owner=user, options=formset.cleaned_data)
        self.assertEqual(new_question, Question.objects.first())

    def test_form_can_have_more_than_two_options(self):
        OptionFormSet=formset_factory(OptionForm, extra=3)
        user=User.objects.create()
        form=newPollForm(data={'question_text': 'test'})
        formset=OptionFormSet(data={'form-1-option_text': 'one', 'form-0-option_text': 'zero',  'form-MAX_NUM_FORMS': '1000', 'form-TOTAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-INITIAL_FORMS': '0', 'form-2-option_text': 'two',})
        self.assertTrue(form.is_valid())
        new_question=form.save(owner=user, options=formset.cleaned_data)
        self.assertEqual(new_question, Question.objects.first())
        self.assertEqual(3, Options.objects.count())
