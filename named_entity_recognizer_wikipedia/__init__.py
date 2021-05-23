from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = 'gdfjkgfjgfdhjkgahjkewqohpiewiozc23834289wjiojfj'

DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

db = SQLAlchemy(app)

from named_entity_recognizer_wikipedia import routes, templates, request