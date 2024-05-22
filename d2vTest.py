import gensim
import os

dataset_path = "steam_reviews_small.csv"
model_path = "doc2vec.model"
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

print("\n")
#train_corpus = list(read_corpus())
print("Built the train corpus\n")
#test_corpus = list(read_corpus(tokens_only=True))

#print(train_corpus[0])
#print(test_corpus[0])

model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=2, workers=4)
model.load(model_path)

def get_model(file):
    if not os.path.exists(file):
        print("Doc2Vec model not found. Exiting")
        exit()
    else:
        model.load(model_path)
    return model

#model.build_vocab(train_corpus)
print("Built the vocabulary\n")

#print(f"Word 'monster' appeared {model.wv.get_vecattr('penalty', 'count')} times in the training corpus.")

#model.train(train_corpus, total_examples=model.corpus_count, epochs=5)

print("Trained the model\n")

model.save(model_path)

print(f"Saved model. Model name :'{model_path}'")

if __name__ == "__main__":
    model = get_model(model_path)

    while True:
        raw_query = input("Insert query, press enter to stop: ")

        if not raw_query.strip():
            break