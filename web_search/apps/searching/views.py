from django.views.generic import TemplateView

from search_engine.indexing import Indexer


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        indexer = Indexer('file')
        context['total_doc_count'] = indexer.get_document_count()
        context['fields_in_index'] = indexer.get_field_list()
        context['word_count'] = indexer.get_word_count()
        return context


class SearchHomeView(TemplateView):
    template_name = "search_home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchHomeView, self).get_context_data(*args, **kwargs)
        indexer = Indexer('file')
        context['docs'] = indexer.search('',1)
        return context
