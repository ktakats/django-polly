from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Cookie import SimpleCookie
from polls.models import Question, Options
import json
# Create your tests here.

def create_user(username, password, email):
    """
    Creates a new user
    """
    return User.objects.create_user(username=username, email=email, password=password)

def create_question(questiontext, owner):
    """
    Creates a new question, where the question_text is questiontext, owner is a user.
    """
    return Question.objects.create(question_text=questiontext, owner=owner)

def create_option(question,optiontext, votes):
    """
    Creates an option instance that belong to the question entry.
    """
    return Options.objects.create(question=question, option_text=optiontext, votes=votes)


class HomeViewTests(TestCase):

    def test_home_view(self):
        response=self.client.get(reverse('polly:index'))
        self.assertTemplateUsed(response, 'polly/home.html')

class myPollsViewTests(TestCase):

    def test_myPolls_view_template(self):
        response=self.client.get(reverse('polly:mypolls'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'polly/myPolls.html')

    def test_myPolls_contains_questions(self):
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("Test?", user)
        response=self.client.get(reverse('polly:mypolls'))
        self.assertContains(response, question.question_text)

class NewPollViewTests(TestCase):

    def test_uses_newPoll_template(self):
        response=self.client.get('/newPoll')
        self.assertTemplateUsed(response, 'polly/newPoll.html')

class ViewPollTests(TestCase):

    def test_view_uses_viewPoll_template(self):
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("Test?", user)
        response=self.client.get('/viewPoll/1')
        self.assertTemplateUsed(response, 'polly/viewPoll.html')

    def test_view_shows_error_if_poll_doesnot_exist(self):
        response=self.client.get('/viewPoll/1')
        self.assertContains(response, "Poll does not exist!")

    def test_after_voting_results_show_up(self):
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("Test?", user)
        self.client.cookies=SimpleCookie({'voted%d' % (question.id): True})
        response=self.client.get('/viewPoll/%d' % (question.id))
        self.assertContains(response, 'resultplot')

    def test_after_voting_view_returns_json_data(self):
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("Test?", user)
        op1=create_option(question, 'op1', 1)
        op1=create_option(question, 'op2', 2)
        self.client.cookies=SimpleCookie({'voted%d' % (question.id): True})
        response=self.client.get('/viewPoll/%d' % (question.id))
        expected=json.dumps({'data': [['op2', 2], ['op1', 1]]})
        self.assertEqual(response.context['result'], expected)
