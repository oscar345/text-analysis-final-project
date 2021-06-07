# text-analysis-final-project

**You do not need to start the Core NLP server. This is done inside python.**

## Get the website running for yourself
### Get the required packages
To get the website running, you will need a virtual environment. This way you have the same versions of packages installed as the ones we had installed. 
1. You need to open the terminal in the directory where this repository is cloned.
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
With the packages installed you are able to run the website with the flask backend. This is very simple. You only have to run:
```
$ python3 run.py
```

A server is running now and the terminal provided a URL for you to open in your browser.

## Use this as a script in the terminal
For this you need to get the virtual environment running as well, which is discussed above. Running the script in the terminal can be done with `wikifier.py`, which takes one argument: the path to the .pos file. 
```
$ python3 wikifier.py en.tok.off.pos
```

Features like testing, are not available here. For those you should use the website.

