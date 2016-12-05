from django.contrib.auth.models import User
from rest_framework import serializers
from polls.models import Question, Options



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Options
        fields=('option_text', 'votes')

class QuestionSerializer(serializers.ModelSerializer):
    options=OptionSerializer(many=True)
    owner=serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model=Question
        fields=('question_text', 'pub_date', 'owner', 'options')


    def create(self, validated_data):
        options_data=validated_data.pop('options')
        question=Question.objects.create(**validated_data)
        for option_data in options_data:
            Options.objects.create(question=question, **option_data)
        return question


"""
class OptionSerializer(serializers.HyperlinkedModelSerializer):
    question=serializers.HyperlinkedRelatedField(many=True, view_name='question-detail', read_only=True)

    class Meta:
        model=Options
        fields=('url', 'question', 'option_text', 'votes')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
   options=serializers.HyperlinkedRelatedField(many=True, view_name='option-detail', read_only=True, lookup_field='pk')
   owner=serializers.ReadOnlyField(source='owner.username')

   class Meta:
       model=Question
       fields=('url', 'question_text', 'pub_date', 'owner', 'options')


"""



class UserSerializer(serializers.HyperlinkedModelSerializer):
    polls=serializers.HyperlinkedRelatedField(many=True, view_name='question-detail', read_only=True)

    class Meta:
        model=User
        fields=('url', 'id', 'username', 'polls')
