import sys

from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser

ix = open_dir("indexdir")

# query_str is query string
query_str = 'sample sentence'
# Top 'n' documents as result
topN = 5  # int(sys.argv[2])

with ix.searcher() as searcher:
    query = MultifieldParser(["content", "title"], ix.schema).parse(query_str)
    results = searcher.search(query, limit=topN)
    for result in results:
        print(result['title'], str(result.score), result.highlights("content"))
