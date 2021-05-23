from werkzeug.utils import redirect
from named_entity_recognizer_wikipedia import app
from flask import request, redirect, url_for

@app.post("/process_files")
def process_files():
    text_area_input = request.form.get("text-area-input")
    file_input = request.files["file-input"]
    check_entities = request.form.get("check-entities")
    return redirect(url_for("output"))
