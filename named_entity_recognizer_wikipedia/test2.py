import sys
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize.repp import ReppTokenizer
from nltk.tokenize import TreebankWordTokenizer as twt


def main():
    f = open('document.pos', 'w+')
    input_text = sys.argv[1]
    raw = input_text
    pos_file = list()
    token_num = 0
    span = twt().span_tokenize(raw)
    locations = [location for location in span]
    print(locations)
    for i, sent in enumerate(sent_tokenize(input_text)):
        for j, (token, tag) in enumerate(pos_tag(word_tokenize(sent))):
            token_id = (i + 1) * 1000 + j + 1
            pos_file.append(f"0 0 {token_id} {token} {tag}")
            token_num += 1
            
    f.write("\n".join(pos_file))
    f.close()


if __name__ == "__main__":
    main()
