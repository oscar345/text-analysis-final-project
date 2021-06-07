import sys
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize.repp import *

def main():

    f = open('document.pos', 'w+')
    input_text = sys.argv[1]
    raw = input_text
    input_text_split = input_text.split()
    print(input_text_split)
    sent_token = sent_tokenize(raw)
    sent_tokens_word = []
    for sentences in range(len(sent_token)):
        sent_tokens_word.append(word_tokenize(sent_token[sentences]))

    sents = sent_tokens_word

    for sent in tokenizer.tokenize_sents(sents, keep_token_positions=True): 
        print(sent)   


if __name__ == "__main__":
    main()
