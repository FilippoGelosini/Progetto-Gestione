import gensim
import os
from whoosh.qparser import SimpleParser, MultifieldParser
from whoosh import scoring
import whoosh
import whoosh.index
import whoosh.matching
import pickle

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

#df = pd.read_csv(dataset_path, encoding="ISO-8859-1")

#def read_corpus(tokens_only=False):
#    with smart_open.open(dataset_path, mode="r", encoding="ISO-8859-1") as file:
#        csv_file = csv.reader(file)
#        next(csv_file)
#
#        count = 0
#        for row in csv_file:
#            tokens = gensim.utils.simple_preprocess(row[6])
#            if tokens_only:
#                yield tokens
#            else:
#                yield gensim.models.doc2vec.TaggedDocument(tokens, [count])
#            count +=1

#print("\n")
#train_corpus = list(read_corpus())
#print("Built the train corpus\n")
#test_corpus = list(read_corpus(tokens_only=True))

#print(train_corpus[0])
#print(test_corpus[0])

#model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=2, workers=4)
#model.load(model_path)

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


#model.build_vocab(train_corpus)
#print("Built the vocabulary\n")

#print(f"Word 'monster' appeared {model.wv.get_vecattr('penalty', 'count')} times in the training corpus.")

#model.train(train_corpus, total_examples=model.corpus_count, epochs=5)

#print("Trained the model\n")

#model.save(model_path)

#print(f"Saved model. Model name :'{model_path}'")

if __name__ == "__main__":
    index = whoosh.index.open_dir("index")
    reader = index.reader()
    with open(model_path_pickle, "rb") as file:
        model = pickle.load(file)
    #model = get_model(model_path)
    d2v_search(model, index)