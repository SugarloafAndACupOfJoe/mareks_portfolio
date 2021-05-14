from django import forms
from datetime import date

from my_finances.models import Income


class DateInput(forms.DateInput):
    input_type = 'date'


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time', 'comment']
        # widgets = {
        #     'date': DateInput()
        # }

    date = forms.DateField(widget=DateInput, initial=date.today())
    # comment = forms.CharField(required=False, widget=forms.Textarea(
    #     attrs={
    #         "placeholder": "Gimme some blocky comment",
    #         "class": "some-class-for-html",
    #         "id": "some-id-for-html",
    #         "rows": 10,  # won't work because of crispy
    #         "cols": 10,  # same
    #     }), help_text="This comment is not required", label="Hello world", disabled=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        # comment_char = cleaned_data.get('comment_char')
        # if comment_char and 'Marek says: ' not in comment_char:
        #     cleaned_data['comment_char'] = 'Marek says: ' + comment_char
        #
        # comment = cleaned_data.get('comment')
        # if 'Marek blabbers: ' not in comment:
        #     cleaned_data['comment'] = 'Marek blabber: ' + comment

        return cleaned_data

    def is_valid(self):
        is_valid = super().is_valid()

        # comment = self.cleaned_data.get('comment')
        # if "it's marek's fault" in comment.lower():
        #     self.add_error('comment', 'It is not Marek\'s fault!!!')
        #     is_valid = False

        # form_date = self.cleaned_data.get('date')
        # if (form_date - date.today()).days < 0:
        #     self.add_error('date', 'Income can not be backdated')
        #     is_valid = False

        return is_valid

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Do something here...
        if commit:
            instance.save()
        return instance
