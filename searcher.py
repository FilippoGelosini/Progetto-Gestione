from whoosh.index import open_dir
from whoosh.qparser import SimpleParser, MultifieldParser
from whoosh import scoring 
import os
import pickle

words_path = "title_words.pickle"
main_path = "index"
title_path = "title"
fieldlist = ["id", "date", "hours_played", "is_early_access", "recommendation", "review", "title"]
main_index = None
title_index = None
limit = 10

file = open(words_path, "rb")
title_words = pickle.load(file)
file.close()

def get_index(dir, index_type):
    if not os.path.exists(dir):
        print(f"{index_type} index not found. Exiting")
        exit()
    else:
        ix = open_dir(dir)
        print(f"{index_type} index retrieved")
    return ix

def print_hit_result(hit, reviews):
    if reviews:
        print(f"Review Date: {hit.get('date')}")
        print(f"Playtime: {hit.get('hours_played')} hours")
        print(f"Early Access: {hit.get('is_early_access')}")
        print(f"Recommendation: {hit.get('recommendation')}")
        print(f"Review: {hit.get('review')}")
    
    print(f"Title: {hit.get('title')}")
    print("\n")

def select_index(query):
    tokens = query.lower().split()
    reviews = False

    for token in tokens:
        if token.strip(".,:;/\\\"!?'^£$%&()€*+-#@<>_®™") not in title_words:
            reviews = True

    return reviews

def full_text_search(main_index, title_index):
    while True: 
        raw_query = input("Insert query, press enter to stop: ")

        if not raw_query.strip():
            break

        reviews = select_index(raw_query)

        if reviews:
            parser = MultifieldParser(fieldlist, schema=main_index.schema)
            searcher = main_index.searcher(weighting=scoring.BM25F()) 
        else:
            parser = SimpleParser("title", schema=title_index.schema)
            searcher = title_index.searcher()
        
        query = parser.parse(raw_query)
        results = searcher.search(query, limit=limit, scored=True)

        i = 1
        if results:
            print(f"Results for '{raw_query}': " + "\n")
            for hit in results:
                print(f"{i})")
                i += 1
                print_hit_result(hit, reviews)
        else:
            print(f"No results found for query \"{raw_query}\"")

if __name__ == "__main__":
    main_index = get_index(main_path, "Main")
    title_index = get_index(title_path, "Title")
    full_text_search(main_index, title_index)