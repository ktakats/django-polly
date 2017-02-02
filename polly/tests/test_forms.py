from django.test import TestCase
from polls.models import Question, Options
from polly.forms import newPollForm, OptionForm, viewPollForm
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import QueryDict

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

class VotingFormTest(TestCase):

    def test_form_displays_all_options(self):
        user=User.objects.create()
        q=Question.objects.create(question_text='Proba', owner=user)
        op1=Options.objects.create(question=q, option_text='op1')
        op2=Options.objects.create(question=q, option_text='op2')
        op3=Options.objects.create(question=q, option_text='op3')
        form=viewPollForm(q_id=q.id)
        self.assertIn('op1', form.as_p())
        self.assertIn('op2', form.as_p())
        self.assertIn('op3', form.as_p())

    def test_form_save_function(self):
        user=User.objects.create()
        q=Question.objects.create(question_text='test', owner=user)
        op1=Options.objects.create(question=q, option_text="83")
        op2=Options.objects.create(question=q, option_text="84")
        form=viewPollForm(data={'option_text': op1.id}, q_id=q.id)
        self.assertTrue(form.is_valid())
        form.save()
        op=Options.objects.get(option_text='83')
        self.assertEqual(op.votes, 1)
