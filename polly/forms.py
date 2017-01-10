from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, FormActions, StrictButton
from crispy_forms.layout import Button, Div, Fieldset, Layout, Submit, HTML
from polls.models import Options, Question



class newPollForm(forms.models.ModelForm):
    option_count=forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model=Question
        fields=['question_text']

        widgets={
            'question_text': forms.fields.TextInput(attrs={
                'placeholder': 'Your question'
                }),
            }
        labels={
            'question_text': ''
        }
        error_messages={
            'question_text': {'required': 'You can not have an empty poll question'}
        }

    def __init__(self, *args, **kwargs):
        options_num=2
        super(newPollForm, self).__init__(*args, **kwargs)
        self.fields['option_count'].initial=options_num
        for index in range(int(options_num)):
            self.fields['option_{index}'.format(index=index)]=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Option {index}'.format(index=str(int(index)+1)) }))
            self.fields['option_{index}'.format(index=index)].label=''


        self.helper=FormHelper()
        self.helper.layout=Layout(
            HTML("<p>Question</p>"),
            'question_text',
            Div(
                 HTML("<p>Options</p>"),
                 css_class='input-group col-md-4 col-md-offset-4 col-xs-2 col-xs-offset-4',
                 )
            )

        for i in range(int(options_num)-1):
            self.helper.layout[2].append(FieldWithButtons('option_{i}'.format(i=i), StrictButton("-")),)

        self.helper.layout[2].append(FieldWithButtons('option_1', StrictButton("+", css_class="btn-add")))
        self.helper.layout.append(FormActions(Submit('submit', 'Submit', css_class='btn btn-default'),))

    def save(self, owner):
        data=self.cleaned_data
        time=timezone.now()
        q=Question(question_text=data['question_text'], pub_date=time, owner=owner)
        q.save()
        for i in range(int(data['option_count'])):
            text='option_{i}'.format(i=i)
            Options.objects.create(question=q, option_text=data[text], votes=0)
        return q

class viewPollForm(forms.Form):
    options=forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect, empty_label=None)
    def __init__(self, *args, **kwargs):

        self.qid=kwargs.pop('q_id')
        super(viewPollForm,self).__init__(*args, **kwargs)
        self.fields['options'].queryset=Options.objects.filter(question_id=self.qid)
