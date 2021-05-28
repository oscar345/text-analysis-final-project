from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.text import TokenSearcher
from nltk.wsd import lesk
from nltk import word_tokenize, sent_tokenize, pos_tag
import os
import wikipedia
from collections import Counter
from random import randrange
from nltk.parse import CoreNLPParser
from nltk.wsd import lesk
import subprocess
from time import sleep
from requests.adapters import HTTPAdapter
import socket
import time
import logging
from urllib.parse import urlparse

# sports are required by using the hyponyms of sport
# for animals and entertainment the same thing will be done.

# for the other named entities, we will need to use Core NLP with some
# advanced settings


class NamedEntityRecognizer():
    def __init__(self):
        self.tokens = dict()
        self.named_entities = dict()
        self.reviewed_text_sents = list()
        self.pos_file = str()

    # Functions that were used to create the training set
    def open_dev_files(self, directory_name, file_name):
        opened_files = list()
        for subset in os.listdir(directory_name):
            if not subset.startswith("."):
                for reference_number in os.listdir(f"{directory_name}/"
                                                   f"{subset}"):
                    if not reference_number.startswith("."):
                        with open(f"{directory_name}/{subset}/"
                                  f"{reference_number}/{file_name}", "r") as file:
                            opened_files.append(file.read())
        return opened_files

    def create_training_data_core_NLP(self, ent_file):
        new_training_data_file = list()
        for line in ent_file.split("\n"):
            words = line.split()
            if len(words) == 5:
                training_data_line = f"{words[3]}\t0"
                new_training_data_file.append(training_data_line)
            elif len(words) == 7:
                training_data_line = f"{words[3]}\t{words[5]}"
                new_training_data_file.append(training_data_line)
        return "\n".join(new_training_data_file)

    
    # Here are the functions that will be used to recognize named entities
    def create_pos_file(self, pos_file):
        # TODO : needs some work
        self.pos_file = pos_file

    def add_pos_file(self, pos_file):
        self.pos_file = pos_file

    def get_data_from_file(self):
        sent = list()
        sent_num = 0
        for line in self.pos_file.split('\n'):
            line = line.split()
            if line != [] and sent_num == line[2][0]:
                sent.append(line[3])
                self.tokens[line[2]] = line[3]
            elif line != []:
                self.reviewed_text_sents.append(sent)
                sent.clear()
                sent.append(line[3])
                sent_num += 1
                self.tokens[line[2]] = line[3]
        self.reviewed_text_sents.append(sent)

    def tag_named_entities_Core_NLP(self, url_Core_NLP):
        ner_tagger = CoreNLPParser(url=url_Core_NLP, tagtype="ner")

        # piece of code I stole from github to let flask wait for a
        # request until the core NLP server is ready for one.
        # https://github.com/Lynten/stanford-corenlp/blob/dec81f51b72469877512c78abc45fd2581bd1237/stanfordcorenlp/corenlp.py
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = urlparse(url_Core_NLP).hostname
        time.sleep(1)  # OSX, not tested
        trial = 1
        while sock.connect_ex((host_name, int(url_Core_NLP.split(":")[-1]))):
            if trial > 5:
                raise ValueError('Corenlp server is not available')
            logging.info('Waiting until the server is available.')
            trial += 1
            time.sleep(1)
        logging.info('The server is available.')
        # End of the code i did not write myself.
        tokens = [token for token in self.tokens.values()]
        named_entities = (list(ner_tagger.tag(tokens)))
        token_locations = list(self.tokens.keys())

        for index, token_location in enumerate(token_locations):
            self.named_entities[token_location] = named_entities[index]

    def tag_named_entities_WordNet(self):
        return ""

    def return_reviewed_text_sents(self):
        return self.reviewed_text_sents

    def return_named_entities(self):
        return self.named_entities


class Wikifier():
    def __init__(self, reviewed_text_sents, named_entities):
        self.tokens = list()
        self.named_entities = named_entities
        self.reviewed_text_sents = reviewed_text_sents
        self.pos_file = str()

    def get_summaries(self):
        something = list()
        for named_entity in self.named_entities:
            something = named_entity
        self.named_entities = something
        
        
    def get_right_wiki_page(self):
        #for sent in self.tokens:
        return ""
            
            

    def create_output_file():
        return ""

    def create_html_output():
        return ""