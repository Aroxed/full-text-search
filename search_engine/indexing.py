import os

from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser


class Indexer:
    SOURCES = ['file', 'internet']

    def __init__(self, source='file'):
        CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/search_engine"
        self.source = source if source == 'file' else 'internet'
        self.index_dir = "%s/%s_%s" % (CURRENT_DIR, 'indexdir', self.source)
        self.schema = Schema(title=TEXT(phrase=True, sortable=True, stored=True,
                                        field_boost=2.0, spelling=True, analyzer=StemmingAnalyzer()),
                             url=ID(stored=True),
                             body=TEXT(spelling=True, stored=True, analyzer=StemmingAnalyzer()))
        self.writer = None
        self.ix = None
        self.create_or_open_index()

    def add_document(self, doc, commit=True):
        writer = self.ix.writer()
        writer.add_document(title=doc['title'], url=doc['url'], body=doc['body'])
        if commit:
            writer.commit()

    def commit(self):
        writer = self.ix.writer()
        writer.commit()

    def get_doc(self, url):
        query = MultifieldParser(["url"], self.ix.schema).parse(url)
        return self.ix.searcher().search(query)

    def get_document_count(self):
        return self.ix.searcher().doc_count_all()

    def get_field_list(self):
        return self.schema.names()

    def get_word_count(self):
        return len(list(self.ix.searcher().lexicon("body")))

    def get_doc_list(self, page_number, pagelen=20):
        result = []
        for i, doc in enumerate(self.ix.searcher().documents()):
            if i in range((page_number - 1) * pagelen, (page_number) * pagelen):
                result.append({'index': i, 'title': doc['title'], 'url': doc['url'], 'body': doc['body'][:100]})
        return result

    def search(self, query_str, page_number):
        query = MultifieldParser(["body", "title"], self.ix.schema).parse(query_str)
        docs = self.ix.searcher().search_page(query, page_number, pagelen=20)
        result = []
        for doc in docs:
            result.append({'title': doc['title'], 'url': doc['url'], 'body': doc.highlights("body")})
        return result

    def clean_index(self):
        # self.writer = self.ix.writer()
        if index.exists_in(self.index_dir):
            self.ix = create_in(self.index_dir, self.schema)

    def create_or_open_index(self):
        if index.exists_in(self.index_dir):
            self.ix = index.open_dir(self.index_dir)
        else:
            if not os.path.exists(self.index_dir):
                os.mkdir(self.index_dir)
            self.ix = create_in(self.index_dir, self.schema)
