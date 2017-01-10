from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from polls.models import Question, Options
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from forms import newPollForm, viewPollForm
# Create your views here.
import urllib2, urllib


from django.forms.formsets import formset_factory

class HomeView(generic.TemplateView):
    template_name='polly/home.html'

class myPollsView(generic.ListView):
    template_name='polly/myPolls.html'
    context_object_name='poll_list'

    def get_queryset(self):
        return Question.objects.all()


def create_new_poll(request):
    if request.method=='POST':
        form=newPollForm(data=request.POST)
        if form.is_valid():
            form.save(owner=User(id=1))
            return redirect(reverse('polly:mypolls'))

    else:
        form=newPollForm()
    return render(request, 'polly/newPoll.html', {'form': form})


def show_and_view_poll(request, pk):
    if request.method=='POST':
        form=viewPollForm(request.POST, q_id=pk)
        if form.is_valid():
            data=request.POST
            ops=Options.objects.get(id=data.values()[1])
            ops.votes+=1
            ops.save()
            resp=render(request, 'polly/viewPoll.html',{'question': ops.question, 'form': form})
            resp.set_cookie('voted'+pk, True)


    else:
        try:
            voted=request.COOKIES['voted'+pk]
            resp=render(request, 'polly/viewPoll.html',{'question': 'You already voted'})
        except:
            form=viewPollForm(q_id=pk)
            q=Question.objects.get(id=pk)
            resp=render(request, 'polly/viewPoll.html',{'question': q.question_text, 'form': form})
    return resp
