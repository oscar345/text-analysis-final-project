from werkzeug.utils import redirect
from named_entity_recognizer_wikipedia import app, named_entity_recognizer
from flask import json, request, redirect, url_for, session, jsonify
import os
import time

progress_value = 0


@app.post("/process_files")
def process_files():
    text_area_input = request.form.get("text-area-input")
    file_input = request.files["file-input"]

    NamedEntityRecognizer = named_entity_recognizer.NamedEntityRecognizer()

    upload_file_names = os.listdir(app.config["UPLOAD_FILES"])
    try:
        index_upload_file = int(upload_file_names[-1].replace("upload_file_", "").replace(".txt", "")) + 1
    except IndexError:
        index_upload_file = 0
    filename = f"./named_entity_recognizer_wikipedia/static/upload_files/upload_file_{index_upload_file}.txt"

    if text_area_input:
        NamedEntityRecognizer.create_pos_file()
    elif file_input:
        file_input.save(filename)
        with open(filename, "r") as file:
            NamedEntityRecognizer.add_pos_file(file.read())
            pos_file = file

    global progress_value
    progress_value = 0
    NamedEntityRecognizer.get_data_from_file()
    NamedEntityRecognizer.tag_named_entities_Core_NLP("http://10.211.55.3:9000")
    progress_value = 1
    named_entities = NamedEntityRecognizer.return_named_entities()
    progress_value = 2
    NamedEntityRecognizer.sync_tokens_named_entities()
    progress_value = 3
    sents = NamedEntityRecognizer.return_sents()
    tokens = NamedEntityRecognizer.return_tokens()
    token_positions = NamedEntityRecognizer.return_token_positions()
    progress_value = 4

    Wikifier = named_entity_recognizer.Wikifier(sents, named_entities, pos_file, tokens, token_positions)
    Wikifier.get_right_wiki_page()
    progress_value = 5
    output = Wikifier.create_dict_output()

    session["output"] = output
    return redirect(url_for("output"))


@app.post("/progress")
def progress():
    global progress_value
    return jsonify(progress=progress_value)