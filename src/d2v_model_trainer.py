import gensim
import smart_open
import csv
import time

dataset_path = "steam_reviews_small.csv"
model_path = "doc2vec.model"
fieldlist = ["date", "hours_played", "is_early_access", "recommendation", "review", "title"]
limit = 10

def read_corpus(tokens_only=False):
    with smart_open.open(dataset_path, mode="r", encoding="ISO-8859-1") as file:
        csv_file = csv.reader(file)
        next(csv_file)

        count = 0
        for row in csv_file:
            tokens = gensim.utils.simple_preprocess(row[6])
            if len(tokens) > 10:
                if tokens_only:
                    yield tokens
                else:
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [count])
            count +=1


def build_model(train_corpus):
    model = gensim.models.doc2vec.Doc2Vec(vector_size=200, window=10, min_count=1, epochs=100, workers=60)

    model.build_vocab(train_corpus)
    print("Built the vocabulary\n")

    model.train(train_corpus, total_examples=model.corpus_count, epochs=10)
    print("Trained the model\n")

    model.save(model_path)

    print(f"Saved the model. Model name :'{model_path}'\n")
    return model

if __name__ == "__main__":
    start = time.perf_counter()
    
    train_corpus = list(read_corpus())
    print("Built the train corpus\n")
    model = build_model(train_corpus)

    end = time.perf_counter()
    time = end - start
    print(f"\nElapsed time: {int(time//60)}:{time%60}\n")