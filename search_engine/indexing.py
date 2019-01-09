import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser


class Indexer:
    SOURCES = ['file', 'internet']

    def __init__(self, source='file'):
        CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/search_engine"
        self.source = source if source == 'file' else 'internet'
        self.index_dir = "%s/%s_%s" % (CURRENT_DIR, 'indexdir', self.source)
        self.schema = Schema(title=TEXT(phrase=True, sortable=True, stored=True,
                                   field_boost=2.0, spelling=True, analyzer=StemmingAnalyzer()), url=ID(stored=True),
                        body=TEXT(spelling=True, stored=True, analyzer=StemmingAnalyzer()))
        self.writer = None
        self.ix = None
        self.create_or_open_index()

    def add_document(self, doc):
        writer = self.ix.writer()
        writer.add_document(title=doc['title'], url=doc['url'], body=doc['body'])
        writer.commit(optimize=True)

    def get_document_count(self):
        return self.ix.searcher().doc_count_all()

    def get_field_list(self):
        return self.schema.names()

    def get_word_count(self):
        return len(list(self.ix.searcher().lexicon("body")))

    def search(self, query_str, page_number):
        if not query_str:
            return self.ix.searcher().documents()
        query = MultifieldParser(["body", "title"], self.ix.schema).parse(query_str)
        results = self.ix.searcher().search_page(query, page_number, pagelen=20)
        return results
        #for result in results:
        #    print(result['title'], str(result.score), result.highlights("body"))

    def clean_index(self):
        #self.writer = self.ix.writer()
        if index.exists_in(self.index_dir):
            self.ix = create_in(self.index_dir, self.schema)

    def create_or_open_index(self):
        if index.exists_in(self.index_dir):
            self.ix = index.open_dir(self.index_dir)
        else:
            if not os.path.exists(self.index_dir):
                os.mkdir(self.index_dir)
            self.ix = create_in(self.index_dir, self.schema)