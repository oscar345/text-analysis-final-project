from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.wsd import lesk
from nltk import word_tokenize, sent_tokenize, pos_tag
import os
import sys
import wikipedia
from collections import Counter
from random import randrange
from nltk.parse import CoreNLPParser



