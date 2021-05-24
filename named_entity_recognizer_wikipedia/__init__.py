from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = 'gdfjkgfjgfdhjkgahjkewqohpiewiozc23834289wjiojfj'
app.config["UPLOAD_FILES"] = "./named_entity_recognizer_wikipedia/static/upload_files"

DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

db = SQLAlchemy(app)

from named_entity_recognizer_wikipedia import routes, templates, request