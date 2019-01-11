from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from search_engine.indexing import Indexer
from .forms import SearchForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        indexer = Indexer('file')
        context['total_doc_count'] = indexer.get_document_count()
        context['fields_in_index'] = indexer.get_field_list()
        context['word_count'] = indexer.get_word_count()
        return context


class SearchHomeView(FormView):
    template_name = "search_home.html"
    form_class = SearchForm
    success_url = reverse_lazy("searching:search_home")

    def get_context_data(self, *args, **kwargs):
        context = super(SearchHomeView, self).get_context_data(*args, **kwargs)
        indexer = Indexer('file')
        context['docs'] = indexer.get_doc_list(1)
        return context

    def form_valid(self, form):

        messages.success(self.request, "Found %d documents" % doc_count)
        return super().form_valid(form)