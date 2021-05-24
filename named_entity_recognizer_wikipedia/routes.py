from flask import render_template, redirect
from named_entity_recognizer_wikipedia import app


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
    return render_template("output.html")


@app.route("/check_entities", methods=["GET"])
def check_entities():
    return render_template("check_entities.html")