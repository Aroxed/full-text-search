from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Enter text to search", required=True)

    def __init__(self, query, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Find'))
        self.fields['query'].initial = query
