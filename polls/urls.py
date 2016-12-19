from django.conf.urls import url, include
from polls import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    url(r'^$', views.api_root, name='root'),
    url(r'^polls/$', views.QuestionList.as_view(), name='question-list'),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view(), name='question-detail'),
    url(r'^options/$', views.OptionList.as_view(), name='option-list'),
    url(r'^options/(?P<nm>[0-9]+)/$', views.OptionDetail.as_view(), name='option-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns+=[
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns=format_suffix_patterns(urlpatterns)
