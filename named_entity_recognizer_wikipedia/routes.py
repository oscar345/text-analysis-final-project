from flask import render_template, redirect, session, request
from named_entity_recognizer_wikipedia import app
import jinja2


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/documentation", methods=["GET", "POST"])
def documentation():
    return render_template("documentation.html")


@app.route("/output", methods=["GET"])
def output():
    output = session["output"]
    index_user = session["index_user"]
    is_testing = session["is_testing"]
    return render_template("output.html", output=output.items(), index_user=str(index_user), is_testing=is_testing)


@app.route("/check_entities", methods=["GET"])
def check_entities():
    return render_template("check_entities.html")