from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, FormActions, StrictButton
from crispy_forms.layout import Button, Div, Fieldset, Layout, Submit, HTML

class newPollForm(forms.Form):
    question_text=forms.CharField(label='question', max_length=100, required=True)
    Option1=forms.CharField(label='option', max_length=100, required=True)
    Option2=forms.CharField(label='option', max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(newPollForm, self).__init__(*args, **kwargs)
        self.fields['question_text'].label=''
        self.fields['Option1'].label=''
        self.fields['Option2'].label=''
        self.helper=FormHelper()
        self.helper.form_class='form_horizontal'
        self.helper.layout=Layout(
        HTML("<p>Question</p>"),
         'question_text',
         Div(
         HTML("<p>Options</p>"),
         FieldWithButtons('Option1', StrictButton("-")),
         FieldWithButtons('Option2', StrictButton("+")),
         css_class='input-group col-md-4 col-md-offset-4 col-xs-2 col-xs-offset-4',

         ),
         FormActions(
            Submit('submit', 'Submit', css_class='btn btn-default'),

         )

        )
