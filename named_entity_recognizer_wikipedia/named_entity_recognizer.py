from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.text import TokenSearcher
from nltk.wsd import lesk
from nltk import word_tokenize, sent_tokenize, pos_tag
import os
import wikipedia
from collections import Counter, OrderedDict
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
from fuzzywuzzy import fuzz, process

# sports are required by using the hyponyms of sport
# for animals and entertainment the same thing will be done.

# for the other named entities, we will need to use Core NLP with some
# advanced settings


class NamedEntityRecognizer():
    def __init__(self):
        self.tokens = list()
        self.named_entities = list()
        self.sents = list()
        self.pos_file = list()
        self.token_positions = list()

    # Functions that were used to create the training set
    def open_dev_files(self, directory_name, file_name):
        """
        directory_name -- the name of the directory in which the
        annotated files are located.
        file_name -- the name of the file in which annotations are
        stored
        
        returns -- a list with each file opened as a string.
        """
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
        """
        entfile -- the file in which the annotations are stored
        
        returns -- a string in a format that can be used by Core NLP to
        train a named entity recognizer model
        """
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
        self.pos_file = pos_file.split("\n")

    def get_data_from_file(self):
        """
        this function is responsible for adding information contained
        in the posfile to the instance of NamedEntityRecognizer
        """
        sent = list()
        sent_num = 0
        for line in self.pos_file:
            line = line.split()
            if line == []:
                break
            word = line[3]
            if sent_num == line[2][0]:
                self.token_positions.append(f"{line[0]} {line[1]} {line[2]}")
                sent.append(word)
                self.tokens.append(word)
            else:
                self.token_positions.append(line[2])
                self.sents.append(sent)
                sent.clear()
                sent.append(word)
                sent_num += 1
                self.tokens.append(word)
        self.sents.append(sent)

    def tag_named_entities_Core_NLP(self, url_Core_NLP):
        """
        url_Core_NLP -- the url on which the core nlp server is
        listening. Most of the time this would be localhost:9000
        
        the named entities will be added to the instance of
        NamedEntityRecognizer
        """
        
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
        self.named_entities = list(ner_tagger.tag(self.tokens))
        
    def sync_tokens_named_entities(self):
        for index, token in enumerate(self.tokens):
            if token != self.named_entities[index][0]:
                ne_index = 0
                while self.tokens[index + 1] != self.named_entities[index + ne_index][0]:
                    ne_index += 1
                ne_tag = self.named_entities[index][1]
                del self.named_entities[index:index + ne_index]
                self.named_entities.insert(index, (token, ne_tag))

    def tag_named_entities_WordNet(self):
        return self.named_entities

    def return_sents(self):
        return self.sents

    def return_named_entities(self):
        return self.named_entities

    def return_tokens(self):
        return self.tokens

    def return_token_positions(self):
        return self.token_positions


class Wikifier():
    def __init__(self, sents_text, named_entities, pos_file, tokens, token_positions):
        self.tokens = tokens
        self.named_entities = named_entities
        self.sents_text = sents_text
        self.pos_file = pos_file
        self.token_positions = token_positions
        self.wiki_urls = list()
        self.fullout_tags = {
            "PER": "person",
            "ORG": "organization",
            "COU": "country",
            "CIT": "city",
            "ANI": "animal",
            "SPO": "sport",
            "NAT": "natural place",
            "ENT": "entertainment"
        }

    def check_for_collocation(self, index, category_previous):
        extra_tokens = 0
        while self.named_entities[index + extra_tokens + 1][1] == category_previous:
            extra_tokens += 1
        return extra_tokens

    def get_right_wiki_page(self):
        known = list()
                
        for index, named_entity in enumerate(self.named_entities):
            if index in known:
                continue
            elif named_entity[1] != "0":
                wiki_search_term = named_entity[0]
                extra_tokens = self.check_for_collocation(index, named_entity[1])
                if extra_tokens != 0:
                    tokens_search_term = [named_entity[0]]
                    for i in range(1, extra_tokens + 1):
                        tokens_search_term.append(self.tokens[index + i])
                        known.append(index + i)
                    wiki_search_term = " ".join(tokens_search_term)

                abbreviation = "." in wiki_search_term
                if not abbreviation:
                    print(wiki_search_term)
                    wiki_pages = [str(title) for title in wikipedia.search(wiki_search_term)]
                    print(wiki_pages)
                    if wiki_pages:
                        most_similiar_wiki_page = process.extractOne(wiki_search_term, wiki_pages, scorer=fuzz.ratio)[0]
                else:
                    most_similiar_wiki_page = wiki_search_term
                
                if most_similiar_wiki_page:
                    print(most_similiar_wiki_page)

                    best_wiki_page = str()
                    
                    try:
                        best_wiki_page = wikipedia.page(title=most_similiar_wiki_page, auto_suggest=abbreviation)
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            best_wiki_page = wikipedia.page(title=f"{most_similiar_wiki_page} {self.fullout_tags[named_entity[1]]}")
                        except wikipedia.exceptions.DisambiguationError:
                            print("again ambiguation")
                        except TypeError:
                            print("page id does not exist")
                    except wikipedia.exceptions.PageError:
                        print("page id does not exist")
                    except TypeError:
                        print("page id does not exist")


                    if best_wiki_page:
                        self.wiki_urls.append(best_wiki_page.url)
                    else:
                        self.wiki_urls.append("")
                
                if extra_tokens != 0:
                    for i in range(extra_tokens):
                        self.wiki_urls.append(best_wiki_page.url)
                    
                print(best_wiki_page)
                print("\n\n\n")
            else:
                self.wiki_urls.append("")

    def create_output_file():
        return ""

    def create_dict_output(self):
        output = OrderedDict()
        print(len(self.token_positions), len(self.tokens), len(self.named_entities), len(self.wiki_urls))

        for i, location in enumerate(self.token_positions):
            output[location] = [self.tokens[i], self.named_entities[i][1], self.wiki_urls[i]]
        return output
        
