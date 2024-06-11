from indexer import add_to_index, get_index, main_schema, title_schema
from searcher import full_text_search
from d2v_model_trainer import read_corpus, build_model
from d2v_search import d2v_search
import gensim
import os
from whoosh.index import open_dir

dataset_path = "steam_reviews_small.csv"
words_path = "title_words.pickle"
main_path = "index"
title_path = "title"
fieldlist = ["id", "date", "hours_played", "is_early_access", "recommendation", "review", "title"]
main_index = None
title_index = None
model_path = "doc2vec.model"
limit = 10
title_list = set()
title_words = set()

def load_model():
    if not os.path.exists(model_path):
        train_corpus = list(read_corpus())
        model = build_model(train_corpus)
    else:
        model = gensim.models.doc2vec.Doc2Vec.load(model_path)
        print("Doc2Vec model retrieved")
    return model

def load_index():
    if not os.path.exists(main_path) or not os.path.exists(title_path):
        main_index = get_index(main_path, main_schema, "Main")
        title_index = get_index(title_path, title_schema, "Title")
        add_to_index(main_index, title_index)
    
    main_index = open_dir(main_path)
    title_index = open_dir(title_path)

    return main_index, title_index


if __name__ == "__main__":
    main_index, title_index = load_index()

    model = load_model()

    while True:
        print("\nSelect the search mode:")
        print("1: Full-Text")
        print("2: Doc2Vec")
        print("0 or enter: Exit")
        search_type = input("\nSelect: ")
        if not search_type.strip():
            break

        search_type = int(search_type)
        
        if search_type == 0:
            break
        if search_type == 1:
            full_text_search(main_index, title_index)
        if search_type == 2:
            d2v_search(model, main_index)
        if search_type < 0 or search_type > 2:
            print("Invalid Choice")