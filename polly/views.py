from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from polls.models import Question
# Create your views here.

class HomeView(generic.TemplateView):
    template_name='polly/home.html'

class myPollsView(generic.ListView):
    template_name='polly/myPolls.html'
    context_object_name='poll_list'

    def get_queryset(self):
        return Question.objects.all()
