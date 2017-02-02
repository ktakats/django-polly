from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from polls.models import Question, Options
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from forms import newPollForm, viewPollForm, OptionForm
from django.forms.formsets import formset_factory
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
    if request.method=='POST':
        form=viewPollForm(request.POST, q_id=pk)
        print request.POST
        print form.is_valid()
        if form.is_valid():
            data=request.POST
    #        ops=Options.objects.get(id=data.values()[1])
    #        ops.votes+=1
    #        ops.save()
            resp=render(request, 'polly/viewPoll.html',{'question': ops.question, 'form': form})
            resp.set_cookie('voted'+pk, True)


    else:
        try:
            voted=request.COOKIES['voted'+pk]
            resp=render(request, 'polly/viewPoll.html',{'question': 'You already voted'})
        except:
            q=Question.objects.get(id=pk)
            form=viewPollForm(q_id=pk)
            print form
            resp=render(request, 'polly/viewPoll.html',{'question': q.question_text, 'form': form})
        #    except DoesNotExist:
        #        pass
    #            resp=render(request, 'polly/viewPoll.html', {'error': })
    return resp
