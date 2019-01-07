import os

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer

def createSearchableData(root):
    '''
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    '''
    schema = Schema(title = TEXT(phrase=True, sortable=True, stored=True,
        field_boost=2.0, spelling=True, analyzer=StemmingAnalyzer()), path=ID(stored=True),
                    content=TEXT(spelling=True, stored=True, analyzer=StemmingAnalyzer()))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    # Creating a index writer to add document as per schema
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    filepaths = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepaths:
        fp = open(path, 'r')
        print(path)
        print(path.split("/")[1].split('.')[0])
        text = fp.read()
        writer.add_document(title=path.split("/")[1].split('.')[0], path=path,
                            content=text)
        fp.close()
    writer.commit()


#root = "crawling/collected"
root = "corpus"
createSearchableData(root)
