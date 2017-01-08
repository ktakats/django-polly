from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Options
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
