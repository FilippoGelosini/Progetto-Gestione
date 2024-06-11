from whoosh.fields import Schema, TEXT, DATETIME, NUMERIC, BOOLEAN
from whoosh.index import create_in, open_dir
from datetime import datetime
import time
import csv
import os
import pickle

dataset_path = "steam_reviews_small.csv"
words_path = "title_words.pickle"
main_path = "index"
title_path = "title"
main_index = None
title_index = None
limit = 10
title_list = set()
title_words = set()

main_schema = Schema(
    id = NUMERIC(stored=True),
    date = DATETIME(stored=True),
    hours_played = NUMERIC(stored=True),
    is_early_access = BOOLEAN(stored=True),
    recommendation = TEXT(stored=True),
    review = TEXT(stored=True),
    title = TEXT(stored=True),
)

title_schema = Schema(
    title = TEXT(stored=True)
)

def get_index(dir, schema_type, index_type):
    if not os.path.exists(dir):
        os.mkdir(dir)
        ix = create_in(dir, schema_type)
        print(f"{index_type} index created")
    else:
        ix = open_dir(dir)
        print(f"{index_type} index retrieved")
    return ix

def add_to_index(main_index, title_index):
    with open(dataset_path, "r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        next(csv_file)
        main_writer = main_index.writer()
        title_writer = title_index.writer()
        counter = 0
        for row in csv_file:
            try:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                playtime = int(row[3])
                early_access = bool(row[4])
                recommendation = row[5]
                review = row[6]
                title = row[7]

                
                main_writer.add_document(id=counter, date=date, hours_played=playtime, is_early_access=early_access, recommendation=recommendation, review=review, title=title)
                print(f"Review added to the index - {counter + 1}")
                counter += 1

                if title not in title_list:
                    title_writer.add_document(title=title)

                title_list.add(title)

                for term in title.lower().split():
                    title_words.add(term.strip(".,:;/\\\"!?'^£$%&()€*+-#@<>_®™"))
            except Exception as e:
                print(f"Error adding document: {e}")
                continue
        main_writer.commit()
        title_writer.commit()

        title_words.remove('')
        with open(words_path, "wb") as file:
            pickle.dump(title_words, file)

if __name__ == "__main__":
    main_index = get_index(main_path, main_schema, "Main")
    title_index = get_index(title_path, title_schema, "Title")

    start = time.perf_counter()
    add_to_index(main_index, title_index)
    end = time.perf_counter()

    time = end - start
    print(f"\nElapsed time: {int(time//60)}:{time%60}\n")