import pickle
import time

from capreolus import Benchmark, Collection, Index, Searcher, Dependency
from capreolus.evaluator import eval_runs,DEFAULT_METRICS

dataset = 'dila'
searcher = 'BM25'
hits = 3
name = f'ds-{dataset}_src-{searcher}_h-{hits}'


@Collection.register
class DilaCollection(Collection):
    module_name = "dila"
    collection_type = "TrecCollection"
    generator_type = "DefaultLuceneDocumentGenerator"
    _path = './dila/data'
    is_large_collection = False
    
    

@Benchmark.register
class DilaBenchmark(Benchmark):
    module_name = "dila"
    dependencies = [Dependency(key="collection", module="collection", name="dila")]
    qrel_file = './dila/dilaqrels.txt'
    topic_file = './dila/dilatopics.txt'
    
    query_type = "title"
    relevance_level = 1
    

collection = Collection.create("dila")
benchmark = Benchmark.create("dila", provide={'collection': collection})
index = Index.create("anserini", {"stemmer": "none" , 'indexstops': False}, provide={"collection": collection})


index.create_index() 


searcher = Searcher.create(searcher, {"hits": hits}, provide={"index": index})


results = {}
n_queries = 0
start = time.time()
for qid, topic in benchmark.topics['title'].items():
        results[qid] = searcher.query(topic)
        n_queries+=1
end = time.time()