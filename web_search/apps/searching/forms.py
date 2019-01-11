from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Enter text to search", required=True)
