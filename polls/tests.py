from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Question, Options


class ApiRootTest(TestCase):
    """
    Tests for the API root.
    """
    def test_api_root_links_exist(self):
        response=self.client.get(reverse('polls:root'))
        self.assertContains(response, 'polls')
        self.assertContains(response, 'users')

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



class QuestionListViewTest(TestCase):
    """
    Tests for the question-list API View.
    """

    def test_question_list_view_with_question(self):
        """
        Create a new question, and user. Test if the question list view in the API contains this question and the user.
        """
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("ListTest", user)
        response=self.client.get(reverse('polls:question-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
        self.assertContains(response, user.username)

    def test_question_list_with_options(self):
        """
        Create a new user and a question, add options to the question, test if the options show up at the question-list API view.
        """
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("ListTest", user)
        option1=create_option(question, 'option1', 2)
        option2=create_option(question, 'option2', 3)
        response=self.client.get(reverse('polls:question-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, option1.option_text)

class QuestionDetailViewTest(TestCase):

    def test_question_detail_view(self):
        user=create_user('test', 'test', 'test@test.com')
        question=create_question("ListTest", user)
        option1=create_option(question, 'option1', 2)
        option2=create_option(question, 'option2', 3)
        response=self.client.get(reverse('polls:question-detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
        self.assertContains(response, option1.option_text)
        self.assertContains(response, option1.option_text)
