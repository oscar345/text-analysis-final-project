from named_entity_recognizer_wikipedia import named_entity_recognizer as \
    ner_mod
import matplotlib.pyplot as plt


def main():
    devfileopener = ner_mod.NamedEntityRecognizer()

    pos_files = devfileopener.open_dev_files("dev", "en.tok.off.pos")
    ent_files = devfileopener.open_dev_files("dev", "en.tok.off.pos.ent")
    progress = 0
    guessed_named_entities_tags = list()
    guessed_urls = list()
    for pos_file in pos_files:
        NERecognizer = ner_mod.NamedEntityRecognizer()
        NERecognizer.add_pos_file(pos_file)
        NERecognizer.get_data_from_file()
        NERecognizer.tag_named_entities_Core_NLP()
        NERecognizer.create_lemma_synsets()
        NERecognizer.tag_named_entities_wordnet()
        NERecognizer.combine_named_entities()
        sents = NERecognizer.return_sents()
        tokens = NERecognizer.return_tokens()
        token_positions = NERecognizer.return_token_positions()
        named_entities = NERecognizer.return_named_entities()
        postags = NERecognizer.return_postags()
        token_char_positions = NERecognizer.return_token_char_positions()    

        Wikifier = ner_mod.Wikifier(
            sents, named_entities, pos_file, tokens, token_positions, postags,
            token_char_positions)
        Wikifier.get_right_wiki_page()
        output = Wikifier.create_dict_output()
        guessed_named_entities_tags.append([named_entity[1] for named_entity
                                            in named_entities])
        guessed_urls.append([value[2] for value in output.values()])
        
        print(progress)
        progress += 1

    anno_named_entities_tags = list()
    anno_urls = list()
    num = 0
    for ent_file in ent_files:
        print(num)
        num += 1
        NERecognizer = ner_mod.NamedEntityRecognizer()
        ent_file_output = NERecognizer.get_data_from_file_ent_file(ent_file)
        anno_named_entities_tags.append(ent_file_output[0])
        anno_urls.append(ent_file_output[1])
    
    guessed_named_entities_tags = [value for items in guessed_named_entities_tags for value in items]
    anno_named_entities_tags = [value for items in anno_named_entities_tags for value in items]
    guessed_urls = [value for items in guessed_urls for value in items]
    anno_urls = [value for items in anno_urls for value in items]
    print(guessed_named_entities_tags)
    print(anno_named_entities_tags)
    print(guessed_urls)
    print(anno_urls)
    results = ner_mod.calculate_scores(guessed_named_entities_tags,
                                       anno_named_entities_tags, guessed_urls,
                                       anno_urls)
    results[0].figure.savefig("./plot.png")
    plt.clf()
    print(results[1], results[2], results[3], results[4])

if __name__ == "__main__":
    main()
