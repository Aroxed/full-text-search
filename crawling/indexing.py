import os

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer


class Indexer():
    def __init__(self):
        schema = Schema(title=TEXT(phrase=True, sortable=True, stored=True,
                                   field_boost=2.0, spelling=True, analyzer=StemmingAnalyzer()), url=ID(stored=True),
                        body=TEXT(spelling=True, stored=True, analyzer=StemmingAnalyzer()))
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")

        # Creating a index writer to add document as per schema
        ix = create_in("indexdir", schema)
        self.writer = ix.writer()

    def add_document(self, doc):
        self.writer.add_document(title=doc['title'], url=doc['url'], body=doc['body'])
        self.writer.commit(optimize=True)

