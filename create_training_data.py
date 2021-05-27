from named_entity_recognizer_wikipedia import named_entity_recognizer
import sys


def main(arguments):
    NamedEntityRecognizer = named_entity_recognizer.NamedEntityRecognizer()
    ent_files = NamedEntityRecognizer.open_dev_files(arguments[1], "en.tok.off.pos.ent")
    for ent_file in ent_files:
        print(NamedEntityRecognizer.create_training_data_core_NLP(ent_file))


if __name__ == "__main__":
    main(sys.argv)
