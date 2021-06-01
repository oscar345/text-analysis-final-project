# text-analysis-final-project

## Get the website running for yourself
### Get the required packages
To get the website running, you will need a virtual environment. This way you have the same versions of packages installed as the ones we had installed. 
1. You need to open the terminal in cloned repository.
2. Run the following command to create a virtual environment: 
```
$ python3 -m venv env
```
3. Activate the virtual environment, by running the next command:
```
$ source env/bin/activate
```
4. Now you will need to install the packages, by running:
```
$ pip3 install -r requirements.txt
```

### Open the website
With the packages install you are able to run the website with the flask backend. This is very simple. You only have to run:
```
$ python3 run.py
```

A server is running now and the terminal provided a URL for you to open in your browser.

## Use this as a script in the terminal
For this you need to get the virtual environment running as well, which is discussed above. Running the script in the terminal can be done with `wikifier.py`, which takes one argument: the path to the .pos file. 
```
$ python3 wikfier.py en.tok.off.pos
```

Features like testing testing and chosing the categories the Wordnet tagger should look for, are not available here. For those you should use the website.

## Get Core NLP running
This is necessary for both the script and the website to process tagging the files. It will tag most of the persons and countries named in the pos files. Add the `server.properties` and the `.ner-model.ser.gz` files in your Stanford Core NLP directory. Open this directory in your terminal and enter the following command:
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -host "0.0.0.0" -serverProperties server.properties
```

A server will start listening and is now accessible by the python scripts, hopefully. If an error occurs that the Core NLP server is not accessible, you should open `request.py` when using the website and `wikifier.py` when using the script. In those scripts this function is run:
```
NERecognizer.tag_named_entities_Core_NLP("http://localhost:9000")
```
Running Core NLP on another system (like a virtual machine) than the Flask server or `wikifier.py`, will require you to replace localhost with your local ip address (this connects your computer with your router).
