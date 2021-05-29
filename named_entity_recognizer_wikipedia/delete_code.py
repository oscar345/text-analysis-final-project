def run_core_NLP_server(self, coreNLPpath):
    try:
        bash_command = f'cd "{coreNLPpath}" ; cat > iamhere.txt ; java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 &'

        os.system(bash_command)
        return "We have succesfully started the server for you"
    except:
        return ("We could not start the server for you. Please do this"
                "manually")
        
        

best_ratio_score = 0
for wiki_page in wiki_pages:
    try:
        if fuzz.token_set_ratio(wikipedia.summary(wiki_page), text) > best_ratio_score:
            best_wiki_page = wiki_page
    except wikipedia.exceptions.DisambiguationError:
        continue
    except wikipedia.exceptions.PageError:
        continue