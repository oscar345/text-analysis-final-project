import sys
from nltk import word_tokenize, sent_tokenize, pos_tag

def main():
    
    f = open('document.pos', 'w+')
    input_text = sys.argv[1]
    raw = input_text
    input_text_split = input_text.split()
    token = word_tokenize(raw)
    sent_token = sent_tokenize(raw)
    print(sent_token)
    
    word_tag = pos_tag(token)
    
    for x, y in word_tag:
        f.write(x+" "+y+"\n")
        for i in range(len(sent_token)):
            if x in sent_token[i]:
                print(i+100)
                print(sent_tokenize.index(x))
        print(raw.index(x), raw.index(x[-1]),x, y)
    f.close()
    

if __name__ == "__main__":
    main()