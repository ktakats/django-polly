from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from polls.models import Question
from forms import newPollForm
# Create your views here.

class HomeView(generic.TemplateView):
    template_name='polly/home.html'

class myPollsView(generic.ListView):
    template_name='polly/myPolls.html'
    context_object_name='poll_list'

    def get_queryset(self):
        return Question.objects.all()

def create_new_poll(request):
    if request.method=='POST':
        form=newPollForm(request.POST)
        if form.is_valid():
            print request.POST
    else:
        form=newPollForm()
        print form
    return render(request, 'polly/newPoll.html', {'form': form,})
