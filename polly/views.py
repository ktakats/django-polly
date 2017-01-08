from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from polls.models import Question, Options
from django.contrib.auth.models import User
from forms import newPollForm, viewPollForm# OptionFormSet
# Create your views here.
import urllib2, urllib
from datetime import datetime

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
        print request
        form=newPollForm(request.POST)
    #    formset=OptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            print request.POST
            data=request.POST
            myoptions=[]
            time=datetime.now()
            me=User(id=1)
            for i in data:
                if i[:6]=="Option":
                    myoptions.append({"option_text": data[i], "votes": 0})
            q=Question(question_text=data['question_text'], pub_date=time, owner=me)
            q.save()
            for option_data in myoptions:
                Options.objects.create(question=q, option_text=option_data['option_text'], votes=0)
            #post_data=[("question_text", data['question_text']), ("options", options), ("pub_date", time), ("owner", me)]
            #result=urllib2.urlopen('localhost:8000/api/polls/', urllib.urlencode(post_data))
            #print result.read()
            return render(request, 'polly/myPolls.html')

    else:
        form=newPollForm()
    #    formset=OptionFormSet(instance=Options())
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
