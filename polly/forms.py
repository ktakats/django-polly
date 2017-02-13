from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, FormActions, StrictButton, Field, InlineRadios
from crispy_forms.layout import Button, Div, Fieldset, Layout, Submit, HTML
from polls.models import Options, Question
from django.contrib.auth.models import User


class OptionForm(forms.models.ModelForm):

    class Meta:
        model=Options
        fields=['option_text']

        labels={
            'option_text': '',
        }

    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.layout=Layout(

            Div('option_text', css_class="optionfield col-md-4 col-md-offset-4 col-xs-2 col-xs-offset-4")

        )


class newPollForm(forms.models.ModelForm):
    #option_count=forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model=Question
        fields=['question_text']

        widgets={
            'question_text': forms.fields.TextInput(attrs={
                'placeholder': 'Your question',
                }),
            }
        labels={
            'question_text': ''
        }
        error_messages={
            'question_text': {'required': 'You can not have an empty poll question'}
        }

    def save(self, owner, options):
        data=self.cleaned_data
        time=timezone.now()
        q=Question(question_text=data['question_text'], pub_date=time, owner=owner)
        q.save()
        for i in range(len(options)):
            Options.objects.create(question=q, option_text=options[i]['option_text'], votes=0)
        return q


class viewPollForm(OptionForm):

    option_text=forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect, empty_label=None)

    def __init__(self, *args, **kwargs):
        self.qid=kwargs.pop('q_id')
        super(viewPollForm,self).__init__(*args, **kwargs)
        self.fields['option_text'].queryset=Options.objects.filter(question_id=self.qid)

    def save(self):
        option=self.cleaned_data['option_text']
        option.votes+=1
        option.save()
        return option

class RegisterForm(forms.models.ModelForm):

    class Meta:
        model=User
        fields=['username', 'email', 'password']
        widgets={
            'username': forms.fields.TextInput(attrs={
                'placeholder': 'username',
                }),
            'email': forms.fields.EmailInput(attrs={
                'placeholder': 'email',
                }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'password',
                }),
            }
        error_messages={
            'username': {'required': "Username is missing", 'unique': "Username already exists."},
            'email': {'required': "Email is missing"},
            'password': {'required': "Password is missing"}
        }

    def clean_email(self):
        email=self.cleaned_data.get('email')
        username=self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email address already exists.')
        return email
