from named_entity_recognizer_wikipedia import named_entity_recognizer

def main():
    output_named_entity = named_entity_recognizer.NamedEntityRecognizer()
    with open('/mnt/c/Users/nooro/OneDrive/Documenten/Studeren/Project analysis/project-text-analysis-assignment-5/Annotations_Gold_Standard/p06/d0246/en.tok.off.pos', 'r') as file:
        output_named_entity.add_pos_file(file.read())
    output_named_entity.get_data_from_file()
    output_named_entity.tag_named_entities_WordNet()
    print(output_named_entity.synset_list())
    
if __name__ == "__main__":
    main()