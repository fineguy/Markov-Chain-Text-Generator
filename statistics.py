# -*- coding: utf-8 -*-
"""
Create dictoinary with key-value pairs like:
(previos word, current word) -> list of possible words (could be repetetive)

We don't account for any punctuation makrs except for periods.
"""

import json
import os
import re
import time

PATH_TO_CORPUS = "./corpus"


def file_iterator(path_to_corpus):
    for author in os.listdir(path_to_corpus):
        path_to_author = os.path.join(path_to_corpus, author)
        if os.path.isdir(path_to_author):
            for book in os.listdir(path_to_author):
                yield open(os.path.join(path_to_author, book), 'r')


def word_iterator(File):
    for line in File:
        for word in re.sub("[^\w\.\']", " ", line).split():
            if word[-1] == ".":
                word = word[:-1]
                yield "."
            yield word.lower()


def count_statistics(path_to_corpus):
    data = {}

    for File in file_iterator(path_to_corpus):
        words = word_iterator(File)
        prev_word = words.next()
        curr_word = words.next()

        for next_word in words:
            key = prev_word + " " + curr_word

            if key in data:
                data[key].append(next_word)
            else:
                data[key] = [next_word]

            prev_word = curr_word
            curr_word = next_word

    return data


def main():
    time_begin = time.time()
    data = count_statistics(PATH_TO_CORPUS)

    with open("statistics.json", "w") as fp:
        json.dump(data, fp)

    print("Finished in %.6f seconds" % (time.time() - time_begin))


if __name__ == '__main__':
    main()