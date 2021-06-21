from capreolus import Benchmark, Collection, Index, Searcher, Dependency ,get_logger
from capreolus.evaluator import eval_runs,DEFAULT_METRICS


@Collection.register
class DilaCollection(Collection):
    module_name = "dila"
    collection_type = "TrecCollection"
    generator_type = "DefaultLuceneDocumentGenerator"
    _path = './data'
    is_large_collection = False
    
    
@Benchmark.register
class DilaBenchmark(Benchmark):
    module_name = "dila"
    dependencies = [Dependency(key="collection", module="collection", name="dila")]
    qrel_file = './tinyqrels.txt'
    topic_file = './tinytopics.txt'
    
    query_type = "title"
    relevance_level = 2
    

collection = Collection.create("dila")
benchmark = Benchmark.create("dila", provide={'collection': collection})
index = Index.create("anserini", {"stemmer": "none"}, provide={"collection": collection})

index.create_index() 

searcher = Searcher.create('BM25', {"hits": 3}, provide={"index": index})

results ={}
for qid, topic in benchmark.topics['title'].items():
        results[qid] = searcher.query(topic)
        

results = eval_runs(results, benchmark.qrels, metrics = DEFAULT_METRICS)

print(results)


