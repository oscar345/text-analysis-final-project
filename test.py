from named_entity_recognizer_wikipedia import named_entity_recognizer

def main():
    output_named_entity = named_entity_recognizer.NamedEntityRecognizer()
    with open('/Users/oscarzwagers/Documents/Text Analysis/Week 5 Text Analysis/project-text-analysis-assignment-5/Annotations_Gold_Standard/p07/d0386/en.tok.off.poskopie', 'r') as file:
        output_named_entity.add_pos_file(file.read())
    output_named_entity.get_data_from_file()
    output_named_entity.tag_named_entities_Core_NLP("http://10.211.55.3:9000")
    output_named_entity.sync_tokens_named_entities()
    output_named_entity.create_lemma_synsets()
    output_named_entity.tag_named_entities_wordnet()
    output_named_entity.combine_named_entities()
    print(output_named_entity.return_named_entities())
    
    
if __name__ == "__main__":
    main()