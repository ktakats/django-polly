from django.conf.urls import url
from . import views

app_name="polly"

urlpatterns=[
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^myPolls$', views.myPollsView.as_view(), name='mypolls'),
    url(r'^newPoll$', views.create_new_poll, name='newpoll'),
    url(r'^viewPoll/(?P<pk>[0-9]+)$', views.show_and_view_poll, name='vote'),
]
