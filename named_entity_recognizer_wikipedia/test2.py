import sys
from nltk import word_tokenize, sent_tokenize, pos_tag

def main():
    
    f = open('document.pos', 'w+')
    input_text = sys.argv[1]
    raw = input_text
    input_text_split = input_text.split()
    token = word_tokenize(raw)
    sent_token = sent_tokenize(raw)
    sent_tokens_word = []
    for sentences in range(len(sent_token)):
        sent_tokens_word.append(word_tokenize(sent_token[sentences]))
    
    begin_list = []
    end_list = []
    word_tag = pos_tag(token)
    for x, y in word_tag:
        f.write(x+" "+y+"\n")

        for i in range(len(sent_token)):
            if x in sent_token[i]:
                sentence_number = ((i+1)*1000 + sent_tokens_word[i].index(x) + 1)
                sent_tokens_word[i].pop(sent_tokens_word[i].index(x))
                #print(sent_tokens_word)
        print(raw.index(x), raw.index(x[-1]), sentence_number, x, y)
    f.close()
    

if __name__ == "__main__":
    main()