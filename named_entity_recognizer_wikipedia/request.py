from werkzeug.utils import redirect
from named_entity_recognizer_wikipedia import app
from flask import request, redirect, url_for
import os
import re


@app.post("/process_files")
def process_files():
    text_area_input = request.form.get("text-area-input")
    file_input = request.files["file-input"]
    check_entities = request.form.get("check-entities")

    upload_file_names = os.listdir(app.config["UPLOAD_FILES"])
    try:
        index_upload_file = int(upload_file_names[-1].replace("upload_file_", "").replace(".txt", "")) + 1
    except IndexError:
        index_upload_file = 0
    filename = f"./named_entity_recognizer_wikipedia/static/upload_files/upload_file_{index_upload_file}.txt"

    if text_area_input:
        with open(filename, "w") as text_file:
            text_file.write(text_area_input)

    if file_input:
        file_input.save(filename)

    if check_entities is not None:
        return redirect(url_for("check_entities"))

    return redirect(url_for("output"))
