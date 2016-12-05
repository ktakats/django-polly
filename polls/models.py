from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime

# Create your models here.
@python_2_unicode_compatible
class Question(models.Model):
    def __str__(self):
        return self.question_text

    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published', default=timezone.now)
    owner=models.ForeignKey('auth.User', related_name='polls')

@python_2_unicode_compatible
class Options(models.Model):
    def __str__(self):
        return self.option_text

    question=models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
