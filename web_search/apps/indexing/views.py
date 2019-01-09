from apps.indexing.forms import FileIndexForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from search_engine.indexing import Indexer


class FileIndexView(FormView):
    template_name = "file_index.html"

    form_class = FileIndexForm
    success_url = reverse_lazy("indexing:file_index")

    @staticmethod
    def file_to_string(f):
        s = []
        for chunk in f.chunks():
           s.append(chunk)
        return s[0].decode('utf-8')

    def form_valid(self, form):
        the_file = self.request.FILES['text_file'] if self.request.FILES['text_file'] else None
        if the_file:
            file_as_string = self.file_to_string(the_file)
            doc = {'body': file_as_string, 'url': '', 'title': ''}
            Indexer('file').add_document(doc)
            messages.success(self.request, "Index was cleaned successfully")
        return super().form_valid(form)


def file_index_clean(request):
    Indexer('file').clean_index()
    messages.success(request, "Index was cleaned successfully")
    return HttpResponseRedirect(reverse_lazy("indexing:file_index"))
