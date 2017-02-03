from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from polls.models import Question, Options
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from forms import newPollForm, viewPollForm, OptionForm
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
import urllib2, urllib
import json


from django.forms.formsets import formset_factory

class HomeView(generic.TemplateView):
    template_name='polly/home.html'

class myPollsView(generic.ListView):
    template_name='polly/myPolls.html'
    context_object_name='poll_list'

    def get_queryset(self):
        return Question.objects.all()


def create_new_poll(request):
    OptionFormSet=formset_factory(OptionForm, extra=2)
    if request.method=='POST':
        form=newPollForm(data=request.POST)
        formset=OptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            options=formset.cleaned_data
            owner=User.objects.get(username='admin')
            form.save(owner=owner, options=options)
        return redirect(reverse('polly:mypolls'))

    else:
        form=newPollForm()
        formset=OptionFormSet()
    return render(request, 'polly/newPoll.html', {'form': form, 'formset': formset})


def show_and_view_poll(request, pk):
    try:
        q=Question.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'polly/viewPoll.html', {'error_message': "Poll does not exist!"})

    if request.method=='POST':
        form=viewPollForm(request.POST, q_id=pk)
        if form.is_valid():
            form.save()
            resp=render(request, 'polly/viewPoll.html',{'question': q.question_text, 'form': form})
            resp.set_cookie('voted'+pk, True)
    else:
        try:
            voted=request.COOKIES['voted'+pk]
            ops=Options.objects.filter(question_id=pk)
            result=json.dumps({op.option_text: op.votes for op in ops})
            resp=render(request, 'polly/viewPoll.html',{'question': q.question_text, 'result': result})
        except:
            form=viewPollForm(q_id=pk)
            resp=render(request, 'polly/viewPoll.html',{'question': q.question_text, 'form': form})

    return resp
