# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:31:12 2015

@author: timasemenov
"""

import json
import random
import time

PATH_TO_STATISTICS = "./statistics.json"


class TextGenerator:
    def __init__(self):
        self.__data = {}
        self.__seed = 1337
        self.__pairs = []
        self.__words_count = 0

    def load_json_data(self, path_to_data):
        with open(path_to_data, 'r') as fp:
            self.__data = json.load(fp)
        self.__pairs = self.__data.keys()

    def set_seed(self, seed):
        self.__seed = seed

    def generate(self, length=30):
        text = ""
        self.__words_count = 0
        pair = random.choice(self.__pairs)

        while self.__words_count < length:
            sentence, pair = self.__generate_sentence(pair)
            text += sentence + " "

        return text

    def __random_word(self, base_pair):
        self.__words_count += 1
        return random.choice(self.__data[base_pair])

    def __random_pair(self, base_pair):
        first_word = self.__random_word(base_pair)
        second_word = self.__random_word(base_pair.split()[1] + " " + first_word)
        return first_word + " " + second_word

    def __generate_sentence(self, pair):
        pair = self.__random_pair(pair)
        sentence = pair.capitalize()
        next_word = self.__random_word(pair)

        while next_word != ".":
            sentence += " " + next_word
            pair = pair.split()[1] + " " + next_word
            next_word = self.__random_word(pair)

        sentence += "."
        return sentence, pair


def main():
    start_time = time.time()
    text_generator = TextGenerator()
    text_generator.load_json_data(PATH_TO_STATISTICS)
    text_generator.set_seed(1337)

    text = text_generator.generate(10000)

    with open("sample_text.txt", "w") as txt:
        txt.write(text)

    print("Finished generating text in %.6f seconds" % (time.time() - start_time))


if __name__ == "__main__":
    main()