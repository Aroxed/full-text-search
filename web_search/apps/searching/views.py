from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
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


class SearchHomeView(ListView):
    context_object_name = 'docs'
    template_name = "search_home.html"
    query = ''
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SearchHomeView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.query)
        # this parameter goes for the right pagination
        context['search_request'] = ('query=' + self.query)
        return context

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('query', '')
        return super(SearchHomeView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        indexer = Indexer('file')
        docs = indexer.search(self.request.GET['query'], 1) if self.query else indexer.get_doc_list(1)
        messages.success(self.request, "Found %d documents" % len(docs))
        return docs


class DocDetailView(DetailView):

    template_name = "doc_view.html"

    def get_object(self):
        indexer = Indexer('file')
        docs = indexer.get_doc(url=self.request.resolver_match.kwargs['url'])
        return docs[0] if len(docs) > 0 else {}
