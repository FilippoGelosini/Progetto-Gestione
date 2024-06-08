import gensim
import os
from whoosh.qparser import MultifieldParser
import whoosh
import whoosh.index
import whoosh.matching

dataset_path = "steam_reviews_small.csv"
model_path = "doc2vec.model"
model_path_pickle = "doc2vec.model.pickle"
words_path = "title_words.pickle"
main_path = "index"
title_path = "title"
fieldlist = ["date", "hours_played", "is_early_access", "recommendation", "review", "title"]
main_index = None
title_index = None
limit = 10

def get_model(file):
    if not os.path.exists(file):
        print("Doc2Vec model not found. Exiting")
        exit()
    else:
        model = gensim.models.doc2vec.Doc2Vec.load(model_path)
        print("Doc2Vec model retrieved")
    return model

def print_hit_result(hit, score):
    print(f"Review Date: {hit.get('date')}")
    print(f"Playtime: {hit.get('hours_played')} hours")
    print(f"Early Access: {hit.get('is_early_access')}")
    print(f"Recommendation: {hit.get('recommendation')}")
    print(f"Review: {hit.get('review')}")
    print(f"Title: {hit.get('title')}")
    print(f"Similarity Score: {score}")
    print("\n")

def d2v_search(model, index):
    while True:
        raw_query = input("Insert query, press enter to stop: ")

        if not raw_query.strip():
            break

        tokens = gensim.utils.simple_preprocess(raw_query)
        inferred_vector = model.infer_vector(tokens)
        sims = model.dv.most_similar([inferred_vector])

        i = 1
        for hit in sims:
            id = "id:" + str(hit[0])
            parser = MultifieldParser(fieldlist, schema=index.schema)
            searcher = index.searcher()
            query = parser.parse(id)
            results = searcher.search(query, limit=1, scored=True)
            print(f"{i})")
            i += 1
            print_hit_result(results[0], hit[1])

if __name__ == "__main__":
    index = whoosh.index.open_dir("index")
    reader = index.reader()
    model = get_model(model_path)
    d2v_search(model, index)