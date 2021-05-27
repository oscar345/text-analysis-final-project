from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = 'gdfjkgfjgfdhjkgahjkewqohpiewiozc23834289wjiojfj'
app.config["UPLOAD_FILES"] = "./named_entity_recognizer_wikipedia/static/upload_files"

from named_entity_recognizer_wikipedia import routes, templates, request