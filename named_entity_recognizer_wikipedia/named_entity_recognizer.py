import matplotlib.pyplot as plt
import matplotlib
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.wsd import lesk
from nltk import word_tokenize, sent_tokenize, pos_tag
import os
import nltk
import wikipedia
from collections import OrderedDict, Counter
from nltk.tag.stanford import StanfordNERTagger
from urllib.parse import urlparse
from fuzzywuzzy import fuzz, process
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import seaborn as sns
from nltk.metrics import ConfusionMatrix

matplotlib.use("Agg")
# Otherwise an assetion CAN occur, not all the time though


class NamedEntityRecognizer():
    def __init__(self):
        """
        This class is responsible for the named entities.

        Attributes
        ----------
        tokens (list): all tokens as list

        named_entities (list): tuples with token and namedentity tag in
        list

        sents (list): all sents of pos file in a list

        pos_file (list): the pos file saved as a list for each line

        token_positions (list): the first three columns of the pos file

        list_of_synsets (list): all synsets found for the tokens

        wordnet_named_entities (list): named entities but from wordnet

        Methods
        -------
        open_dev_files(self, directory_name, file_name):
            Opens all the ent files and returns them as a list.

        create_training_data_core_NLP(self, ent_file):
            Takes one entfile to return a string in the layout for Core
            NLP

        create_pos_file(self, pos_file):
            when a string is given, a posfile is created for further
            processing

        add_pos_file(self, pos_file):
            adding a posfile to the instance of the class

        get_data_from_file(self):
            reading the pos file so all necessary data is extracted

        tag_named_entities_Core_NLP(self, url_Core_NLP):
            using the Core NLP server and a trained model to tag named
            entities

        create_lemma_synsets(self):
            to use wordnet lemmas are necessary to get the right synsets

        tag_named_entities_wordnet(self, categories=["animal", "sport",
                                                     "entertainment"]):
            using wordnet to tag named entities that might be hyponyms
            of the categories

        combine_named_entities(self):
            combines wordnet and Core NLP named entities when wordnet is
            used in addition to Core NLP
        """

        self.tokens = list()
        self.named_entities = list()
        self.sents = list()
        self.pos_file = list()
        self.token_positions = list()
        self.list_of_synsets = list()
        self.wordnet_named_entities = list()
        self.pos_tags_pos = list()
        self.token_char_positions = list()
        
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

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
                                  f"{reference_number}/{file_name}", "r") as \
                                      file:
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
    def create_pos_file(self, raw_text):
        pos_file = list()
        token_num = 0
        for i, sent in enumerate(sent_tokenize(raw_text)):
            for j, (token, tag) in enumerate(pos_tag(word_tokenize(sent))):
                token_id = (i + 1) * 1000 + j + 1
                pos_file.append(f"0 0 {token_id} {token} {tag}")
                token_num += 1
        self.pos_file = pos_file

    def add_pos_file(self, pos_file):
        self.pos_file = pos_file.split("\n")

    def get_data_from_file(self):
        """
        this function is responsible for adding information contained
        in the posfile to the instance of NamedEntityRecognizer
        """
        sent = list()
        sent_num = 1
        for line in self.pos_file:
            line = line.split()
            if line == []:
                break
            word = line[3]
            if sent_num == line[2][0]:
                self.token_char_positions.append(f"{line[0]} {line[1]}")
                self.token_positions.append(line[2])
                sent.append(word)
                self.tokens.append(word)
                self.pos_tags_pos.append(line[4])
            else:
                self.token_char_positions.append(f"{line[0]} {line[1]}")
                self.token_positions.append(line[2])
                self.sents.append(sent)
                sent.clear()
                sent.append(word)
                self.pos_tags_pos.append(line[4])
                sent_num += 1
                self.tokens.append(word)
        self.sents.append(sent)

    def get_data_from_file_ent_file(self, entfile):
        """
        get the named entities and the wiki urls from the annotated file
        """
        ent_urls = list()
        ent_tags = list()
        for line in entfile.split("\n"):
            line = line.split()
            if line == []:
                break
            elif len(line) > 5:
                ent_urls.append(line[6])
                ent_tags.append(line[5])
            else:
                ent_urls.append("")
                ent_tags.append("0")
        return ent_tags, ent_urls

    def tag_named_entities_Core_NLP(self):
        """
        url_Core_NLP -- the url on which the core nlp server is
        listening. Most of the time this would be localhost:9000

        the named entities will be added to the instance of
        NamedEntityRecognizer, after they are synced with the tokens.
        Core NLP will tokenize the tokens and those are different from
        the tokens from nltk resulting in two uneven lists, which will
        cause wikipedia urls and named entity tags to be assigned to the
        wrong tokens.
        """

        jar = './Core_NLP_files/stanford-corenlp-4.2.0.jar'
        model = './Core_NLP_files/ner-model.ser.gz'

        ner_tagger = StanfordNERTagger(model, jar, encoding='utf-8')
        self.named_entities = list(ner_tagger.tag(self.tokens))

        for index, token in enumerate(self.tokens):
            if token != self.named_entities[index][0]:
                ne_index = 0
                try:
                    while self.tokens[index + 1] != self.named_entities[index + ne_index][0]:
                        ne_index += 1
                except IndexError:
                    self.tokens = list()
                    self.named_entities = list()
                    self.sents = list()
                    self.pos_file = list()
                    self.token_positions = list()
                    self.list_of_synsets = list()
                    self.wordnet_named_entities = list()
                    self.pos_tags_pos = list()
                    break
                    # core NLP will tokenize the named entities again,
                    # if will not sync with the original tokens, the
                    # program will stop working because of an uneven
                    # amount of items in the lists

                ne_tag = self.named_entities[index][1]
                del self.named_entities[index:index + ne_index]
                self.named_entities.insert(index, (token, ne_tag))

    def create_lemma_synsets(self):
        """
        it will add a list with synsets for each lemmatized token in the
        text if it can find a synset.
        """
        print(len(self.tokens))
        token_pos_tags = pos_tag(self.tokens)
        print(len(token_pos_tags))
        lemmatizer = WordNetLemmatizer()
        for token_pos_tag in token_pos_tags:
            if token_pos_tag[1].startswith('NN'):
                lemma = (lemmatizer.lemmatize(token_pos_tag[0], wordnet.NOUN))
                try:
                    lemma_synsets = (wordnet.synsets(lemma, pos="n"))
                    self.list_of_synsets.append(lemma_synsets)
                except IndexError:
                    self.list_of_synsets.append(None)
            else:
                self.list_of_synsets.append(None)
        print(len(self.list_of_synsets))

    def hypernym_of(self, lemma_synset, hypernym_synset):
        """
        lemma_synset -- the synset of the lemma token. this function
        checks if that token is a hyponym of the synset of one of the
        categories
        hypernym_synset -- the synset of one of the the categories

        returns -- a boolean value, that is true when the lemma was a
        hyponym of the category synset
        """
        if lemma_synset == hypernym_synset:
            return True
        for lemma_hypernym in lemma_synset.hypernyms():
            if hypernym_synset == lemma_hypernym:
                return True
            if self.hypernym_of(lemma_hypernym, hypernym_synset):
                return True
        return False

    def get_category(self, category, hypernym_synset, lemma_synsets, index):
        """
        category -- the category that is checked for being the hypernym
        of the lemma.
        hypernym_synset -- the synset of the category
        lemma_synsets -- all the synsets of the lemma that is checked
        for being the hyponym of the category.
        index -- the index of the token/lemma being checked

        will add the category to self.wordnet_named_entities if the
        lemma is a hyponym of the category.
        """
        right_synset = None
        if len(lemma_synsets) > 1:
            sent_num = int(self.token_positions[index][0])
            right_synset = lesk(self.sents[sent_num], self.tokens[index],
                                synsets=lemma_synsets)
        elif len(lemma_synsets) == 1:
            right_synset = lemma_synsets[0]
        if right_synset is not None and self.hypernym_of(right_synset,
                                                         hypernym_synset):
            self.wordnet_named_entities[index][1] = category

    def tag_named_entities_wordnet(self, categories=["animal", "sport",
                                                     "entertainment"]):
        """
        categories -- the categories the wordnet named entity recognizer
        should look for. There are 7 categories you can choose from:
        country, city, organization, entertainment, animal, sport,
        person. This should be a list.

        the named entities found here will be added to
        self.wordnet_named_entities.
        """
        hypernym_synsets = list()
        for category in categories:
            hypernym_synsets.append(wordnet.synsets(category, pos="n")[0])
        print(len(self.list_of_synsets), len(self.tokens))
        for index, lemma_synsets in enumerate(self.list_of_synsets):
            self.wordnet_named_entities.append([self.tokens[index], "0"])
            if lemma_synsets is not None:
                for i, category in enumerate(categories):
                    self.get_category(category, hypernym_synsets[i],
                                      lemma_synsets, index)
                    if self.wordnet_named_entities[index][1] != "0":
                        break

    def combine_named_entities(self):
        """
        the named entities from wordnet will be added to the named
        entities from Core NLP, when Core NLP does not have a tag and
        wordnet does. When both have a named entity tag, the one from
        Core NLP is kept.
        """
        named_entity_abbreviation = {
            "animal": "ANI",
            "sport": "SPO",
            "entertainment": "ENT",
            "person": "PER",
            "organization": "ORG",
            "country": "COU",
            "city": "CIT"
        }
        for index, named_entity in enumerate(self.named_entities):
            w_named_entity_tag = self.wordnet_named_entities[index][1]
            if named_entity[1] == "0" and w_named_entity_tag != "0":
                self.wordnet_named_entities[index][1] = \
                    named_entity_abbreviation[w_named_entity_tag]
                self.named_entities[index] = self.wordnet_named_entities[index]

    def return_sents(self):
        return self.sents

    def return_named_entities(self):
        return self.named_entities

    def return_wordnet_named_entities(self):
        return self.wordnet_named_entities

    def return_tokens(self):
        return self.tokens

    def return_postags(self):
        return self.pos_tags_pos

    def return_token_positions(self):
        return self.token_positions
    
    def return_token_char_positions(self):
        return self.token_char_positions

    def return_pos_file(self):
        return self.pos_file


class Wikifier():
    def __init__(self, sents_text, named_entities, pos_file, tokens,
                 token_positions, pos_tags_pos, token_char_positions):
        """
        This class and its methods will look for the right wikipedia
        page for a given named entity

        Attributes
        ----------
        tokens (list): all tokens as list

        named_entities (list): tuples with token and namedentity tag in
        list

        sents_text (list): all sents of pos file in a list

        pos_file (list): the pos file saved as a list for each line

        token_positions (list): the first three columns of the pos file

        wiki_urls (list): the wiki url for each token

        fullout_tags -- get whole word for better search wikipedia

        Methods
        -------
        get_right_wiki_page(self):
            Will look up the right wikipedia page for a specific token

        def create_output_file(self):
            making a file in the same layout as an ent file

        def create_dict_output(self):
            returns a dict to make displaying the output on the site
            easier

        """
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
        self.pos_tags_pos = pos_tags_pos
        self.token_char_positions = token_char_positions
        self.output = OrderedDict()

    def check_for_collocation(self, index, category_previous):
        """
        index -- the index of the token being handled
        category_previous -- the tag of the previous token

        returns the number of extra tokens to create the whole named
        entity
        """
        extra_tokens = 0
        try:
            while self.named_entities[index + extra_tokens + 1][1] == \
                    category_previous:
                extra_tokens += 1
        except IndexError:
            print("no extra tokens, because end of file without a dot.")
        return extra_tokens

    def handle_wiki_page_err(self, most_similiar_wiki_page, abbreviation,
                             named_entity):
        """
        most_similiar_wiki_page -- title of a wikipedia page that is
        most similiar to the named entity
        abbreviation -- if it is an abbreviation like "U.S.", wikipedia
        will auto suggest a page
        named_entity -- the tag of the named entity is used in case of a
        disambiguation error. this could help find the right page.

        returns -- the wikipage that the function found
        """
        if most_similiar_wiki_page:
            best_wiki_page = str()

            try:
                best_wiki_page = wikipedia.page(title=most_similiar_wiki_page,
                                                auto_suggest=abbreviation)
            except wikipedia.exceptions.DisambiguationError:
                try:
                    best_wiki_page = wikipedia.page(
                        title=f"{most_similiar_wiki_page} "
                        f"{self.fullout_tags[named_entity[1]]}")
                except wikipedia.exceptions.DisambiguationError:
                    print("again ambiguation")
                except TypeError:
                    print("page id does not exist")
                except wikipedia.exceptions.PageError:
                    print("page id does not exist")
            except wikipedia.exceptions.PageError:
                print("page id does not exist")
            except TypeError:
                print("page id does not exist")

            if best_wiki_page:
                self.wiki_urls.append(best_wiki_page.url)
                return best_wiki_page
            else:
                self.wiki_urls.append("")

    def get_right_wiki_page(self):
        """
        loops over all the tokens to find named entities and collocate
        them (with the 'check_for_collocations function) and handle
        errors (with the handle_wiki_page_err function).
        """
        known = list()

        for index, named_entity in enumerate(self.named_entities):
            if index in known:
                continue
            elif named_entity[1] != "0":
                wiki_search_term = named_entity[0]
                extra_tokens = self.check_for_collocation(index,
                                                          named_entity[1])
                if extra_tokens != 0:
                    tokens_search_term = [named_entity[0]]
                    for i in range(1, extra_tokens + 1):
                        tokens_search_term.append(self.tokens[index + i])
                        known.append(index + i)
                    wiki_search_term = " ".join(tokens_search_term)

                abbreviation = "." in wiki_search_term
                # most abbreviations are found best by wikipedia self.

                if not abbreviation:
                    wiki_pages = [str(title) for title in wikipedia.search(
                        wiki_search_term)]
                    if wiki_pages:
                        most_similiar_wiki_page = process.extractOne(
                            wiki_search_term, wiki_pages, scorer=fuzz.ratio)[0]
                    else:
                        most_similiar_wiki_page = None
                        self.wiki_urls.append("")
                else:
                    most_similiar_wiki_page = wiki_search_term

                if most_similiar_wiki_page is not None:
                    best_wiki_page = self.handle_wiki_page_err(
                        most_similiar_wiki_page, abbreviation, named_entity)
                else:
                    best_wiki_page = None
                # Is done in another method to prevent this method from
                # becoming to large with too much indentation

                if extra_tokens != 0:
                    for i in range(extra_tokens):
                        if best_wiki_page is not None:
                            self.wiki_urls.append(best_wiki_page.url)
                        else:
                            self.wiki_urls.append("")

            else:
                self.wiki_urls.append("")

    def create_output_file(self):
        output_file = list()
        for index, (key, value) in enumerate(self.output.items()):
            if (value[2] == ""):
                output_file.append(f"{self.token_char_positions[index]} {key} {value[0]} {self.pos_tags_pos[index]}")
            else:
                output_file.append(f"{self.token_char_positions[index]} {key} {value[0]} {self.pos_tags_pos[index]} {value[1]} {value[2]}")
        return ("\n").join(output_file)

    def create_dict_output(self):

        for i, location in enumerate(self.token_positions):
            self.output[location] = [self.tokens[i], self.named_entities[i][1],
                                     self.wiki_urls[i]]
        return self.output


def calculate_scores(new_file, annotated_file, guessed_urls, annotated_urls):
    all_labels = new_file + annotated_file
    labels = sorted(list(set(all_labels)))
    cfmsk = confusion_matrix(annotated_file, new_file, labels=labels)
    cfm = ConfusionMatrix(annotated_file, new_file)
    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cfm[i, j]
            else:
                false_negatives[i] += cfm[i, j]
                false_positives[j] += cfm[i, j]

    f_scores = list()
    for i in sorted(labels):
        if true_positives[i] == 0:
            f_scores.append(0)
        else:
            precision = true_positives[i] / float(true_positives[i]
                                                  + false_positives[i])
            recall = true_positives[i] / float(true_positives[i]
                                               + false_negatives[i])
            f_scores.append(2 * (precision * recall) / float(precision
                                                             + recall))
    cfmatrix_img = None
    # For some reason this is neccesary to make sure previous heatmaps
    # dont overlap
    cfmatrix_img = sns.heatmap(cfmsk, annot=True, cmap='Blues',
                               xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Annotated")

    print(annotated_urls)

    correct_urls = len([url for index, url in enumerate(guessed_urls) if url !=
                        "" and annotated_urls[index] == url])
    guessed_urls = len([url for url in guessed_urls if url != ""])
    anno_urls = len([url for url in annotated_urls if url != ""])

    print(correct_urls, guessed_urls, anno_urls)
    accuracy_recall = round(correct_urls / anno_urls * 100, 2)
    accuracy_precision = round(correct_urls / guessed_urls * 100, 2)

    return (cfmatrix_img, f_scores, round(cohen_kappa_score(new_file,
            annotated_file), 3), accuracy_recall, accuracy_precision, labels)
