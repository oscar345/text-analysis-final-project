from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.wsd import lesk
from nltk import word_tokenize, sent_tokenize, pos_tag
import os
import wikipedia
from collections import Counter
from random import randrange
from nltk.parse import CoreNLPParser

# sports are required by using the hyponyms of sport
# for animals and entertainment the same thing will be done.

# for the other named entities, we will need to use Core NLP with some
# advanced settings


class NamedEntityRecognizer():
    def __init__(self):
        self.tokens = list()
        self.named_entities = list()
        self.reviewed_text = str()

    def open_dev_files(self, directory_name, file_name):
        opened_files = list()
        for subset in os.listdir(directory_name):
            if not subset.startswith("."):
                for reference_number in os.listdir(f"{directory_name}/"
                                                   f"{subset}"):
                    if not reference_number.startswith("."):
                        with (open(f"{directory_name}/{subset}/"
                                   f"{reference_number}/{file_name}", "r")
                              as file):
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

    def run_core_NLP_server(self, coreNLPpath):
        try:
            os.system("cd ~")
            os.system(f"cd {coreNLPpath}")
            os.system('java -mx4g -cp "*"'
                      'edu.stanford.nlp.pipeline.StanfordCoreNLPServer'
                      '-preload tokenize,ssplit,pos,lemma,ner,parse,depparse'
                      '-status_port 9000 -port 9000 -timeout 15000 & ')
            return "We have succesfully started the server for you"
        except:
            return ("We could not start the server for you. Please do this"
                    "manually")

    def create_list_tokens_text_input(self, text):
        self.reviewed_text = text
        tokens = self.reviewed_text
        self.tokens = tokens

    def tag_named_entities(self):
        ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype="ner")
        self.named_entities = list(ner_tagger.tag(self.tokens))

    def return_reviewed_text(self):
        return self.reviewed_text

    def return_named_entities(self):
        return self.named_entities


class Wikifier():
    def __init__(self, text, named_entities):
        self.text = text
        self.named_entities = named_entities

    def get_summaries(self):
        something = list()
        for named_entity in self.named_entities:
            something = named_entity
        self.named_entities = something

    def create_output_file():
        return ""

    def create_html_output():
        return ""