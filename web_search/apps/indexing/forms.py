from django import forms


class FileIndexForm(forms.Form):
    text_file = forms.FileField(label="Choose single file to add", required=False)
    text_folder = forms.FileField(label="Choose folder with text files to add", required=False)

    def clean(self):
        hi = self.cleaned_data.get('text_file')
        by = self.cleaned_data.get('text_folder')
        if not hi and not by:
            raise forms.ValidationError('One of the FILE fields is required')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(FileIndexForm, self).__init__(*args, **kwargs)
        self.fields['text_folder'].widget.attrs['directory'] = 'directory'
        self.fields['text_folder'].widget.attrs['webkitdirectory'] = 'webkitdirectory'
        self.fields['text_folder'].widget.attrs['multiple'] = 'multiple'
