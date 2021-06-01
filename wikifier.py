from named_entity_recognizer_wikipedia import named_entity_recognizer as \
    ner_mod
import sys


def main(arguments):
    NERecognizer = ner_mod.NamedEntityRecognizer()

    with open(arguments[1], "r") as file:
        NERecognizer.add_pos_file(file.read())
        pos_file = file

    NERecognizer.get_data_from_file()
    NERecognizer.tag_named_entities_Core_NLP(
        "http://10.211.55.3:9000")
    NERecognizer.create_lemma_synsets()
    NERecognizer.tag_named_entities_wordnet()
    NERecognizer.combine_named_entities()

    sents = NERecognizer.return_sents()
    tokens = NERecognizer.return_tokens()
    token_positions = NERecognizer.return_token_positions()
    named_entities = NERecognizer.return_named_entities()

    Wikifier = ner_mod.Wikifier(
        sents, named_entities, pos_file, tokens, token_positions)
    Wikifier.get_right_wiki_page()
    output = Wikifier.create_dict_output()
    print(output)


if __name__ == "__main__":
    main(sys.argv)
