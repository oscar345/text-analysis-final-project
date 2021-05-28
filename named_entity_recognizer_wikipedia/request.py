from werkzeug.utils import redirect
from named_entity_recognizer_wikipedia import app, named_entity_recognizer
from flask import request, redirect, url_for, session
import os


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
            
    NamedEntityRecognizer.get_data_from_file()
    NamedEntityRecognizer.tag_named_entities_Core_NLP("http://10.211.55.3:9000")
    named_entities = NamedEntityRecognizer.return_named_entities()
    session["named_entities"] = named_entities
    return redirect(url_for("output"))
