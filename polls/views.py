from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from polls.models import Question, Options
from polls.serializers import QuestionSerializer, OptionSerializer, UserSerializer
from polls.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class QuestionList(generics.ListCreateAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class OptionList(generics.ListCreateAPIView):
    queryset=Options.objects.all()
    serializer_class=OptionSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)



class OptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Options.objects.all()
    serializer_class=OptionSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'polls': reverse('question-list', request=request, format=format)
    })
