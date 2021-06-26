from django import forms
from datetime import date

from my_finances.models import Balance, Income, Outcome


class DateInput(forms.DateInput):
    input_type = 'date'


class IncomeOutcomeForm(forms.ModelForm):
    def is_valid(self):
        is_valid = super().is_valid()

        value = self.cleaned_data.get('value')
        form_date = self.cleaned_data.get('date')
        repetitive = self.cleaned_data.get('repetitive')
        repetition_interval = self.cleaned_data.get('repetition_interval')
        repetition_time = self.cleaned_data.get('repetition_time')

        if value <= 0:
            self.add_error('value', 'Value must be a positive number.')
            is_valid = False

        if repetition_interval == 4 and form_date.day > 28:  # if it's MONTHS and date is set for over 28th
            self.add_error('date', 'When repetition interval is set to MONTHS, date dat can not exceed 28.')
            is_valid = False

        if repetitive:
            if repetition_interval == 1:  # if it's N/A
                self.add_error('repetition_interval', 'Repetition interval can not be N/A when Repetition is selected.')
                is_valid = False
            if repetition_time == 0:
                self.add_error('repetition_time', 'Repetition time can not be 0 when Repetition is selected.')
                is_valid = False
        else:  # if Repetition is False
            if repetition_interval != 1:
                self.add_error('repetitive', 'Repetitive needs to be selected when Repetition interval is not N/A.')
                is_valid = False

        return is_valid


class IncomeForm(IncomeOutcomeForm):
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

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Do something here...
        if commit:
            instance.save()
        return instance


class OutcomeForm(IncomeOutcomeForm):
    class Meta:
        model = Outcome
        fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time', 'comment']

    date = forms.DateField(widget=DateInput, initial=date.today())


class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['value', 'date', 'type', 'comment']

    date = forms.DateField(widget=DateInput, initial=date.today())
