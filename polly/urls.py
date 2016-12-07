from django.conf.urls import url
from . import views

app_name="polly"

urlpatterns=[
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^myPolls$', views.myPollsView.as_view()),
]
