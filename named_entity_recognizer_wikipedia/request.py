from werkzeug.utils import redirect, send_file
import wikipedia
from named_entity_recognizer_wikipedia import app, named_entity_recognizer as ner_mod
from flask import json, request, redirect, url_for, session, jsonify, send_file
import os
from pathlib import Path
import matplotlib.pyplot as plt


def create_filenames_and_user_id():
    user_ids = sorted([int(dr.replace("user_upload_", "")) for dr in os.listdir(app.config["USER_UPLOADS"])])
    try:
        index_user = user_ids[-1] + 1
    except IndexError:
        index_user = 0
    create_files = ["pos_file.txt", "progress.txt", "en.tok.off.pos.ent", "test_ent_file.txt"]
    file_path = os.path.join(Path().absolute(), app.config["USER_UPLOADS"], f"user_upload_{index_user}")
    os.mkdir(file_path)
    file_names = [os.path.join(file_path, create_file) for create_file in create_files]
    return file_names, index_user


def write_progress(filename, number):
    with open(filename, "w") as file:
        file.write(number)


def recognize_named_entities(progress_file, categories, NERecognizer):
    write_progress(progress_file, "0")
    NERecognizer.get_data_from_file()
    NERecognizer.tag_named_entities_Core_NLP()
    if categories != []:
        write_progress(progress_file, "1")
        NERecognizer.create_lemma_synsets()
        write_progress(progress_file, "2")
        NERecognizer.tag_named_entities_wordnet(categories=categories)
        write_progress(progress_file, "3")
        NERecognizer.combine_named_entities()
        write_progress(progress_file, "4")

    sents = NERecognizer.return_sents()
    tokens = NERecognizer.return_tokens()
    token_positions = NERecognizer.return_token_positions()
    named_entities = NERecognizer.return_named_entities()
    postags = NERecognizer.return_postags()
    write_progress(progress_file, "5")
    return sents, tokens, token_positions, named_entities, postags


@app.post("/process_files")
def process_files():
    NERecognizer = ner_mod.NamedEntityRecognizer()

    text_area_input = request.form.get("text-area-input")
    file_input = request.files["file-input"]
    categories = request.form.getlist('categories[]')
    test_file_input = request.files["test-file-input"]
    filenames, index_user = create_filenames_and_user_id()
    session["index_user"] = index_user
    
    if text_area_input:
        NERecognizer.create_pos_file(text_area_input)
        pos_file = NERecognizer.return_pos_file()
    elif file_input:
        file_input.save(os.path.join(Path().absolute(), filenames[0]))
        with open(filenames[0], "r") as file:
            NERecognizer.add_pos_file(file.read())
            pos_file = file
        
    sents, tokens, token_positions, named_entities, postags = \
        recognize_named_entities(filenames[1], categories, NERecognizer)

    Wikifier = ner_mod.Wikifier(
        sents, named_entities, pos_file, tokens, token_positions, postags)
    Wikifier.get_right_wiki_page()
    write_progress(filenames[1], "6")
    output = Wikifier.create_dict_output()
    
    with open(filenames[2], "w") as ent_file:
        ent_file.write(Wikifier.create_output_file())
    
    is_testing = False
    if test_file_input:
        is_testing = True
        test_file_input.save(os.path.join(Path().absolute(), filenames[3]))
        with open(filenames[3], "r") as file:
            ent_file_output = NERecognizer.get_data_from_file_ent_file(file.read())        
        named_entities_tags = [named_entity[1] for named_entity in named_entities]
        guessed_urls = [value[2] for value in output.values()]
        results = ner_mod.calculate_scores(named_entities_tags, ent_file_output[0], guessed_urls, ent_file_output[1])
        session["scores"] = [results[1], results[2], results[3], results[4], results[5]]
        results[0].figure.savefig(app.config["USER_UPLOADS"] + f"user_upload_{index_user}" + "/plot.png")
        plt.clf()

        
    session["is_testing"] = is_testing
    session["output"] = output
    return redirect(url_for("output"))


@app.post("/progress")
def progress():
    index_user = session["index_user"]
    progress_name = app.config["USER_UPLOADS"] \
        + f"user_upload_{index_user + 1}/progress.txt"
    with open(progress_name, "r") as file:
        progress = file.read()
    return jsonify(progress=progress)


@app.route('/download_file/<index_user>')
def download_file(index_user):
    filename = f"./static/user_files/user_upload_{index_user}/en.tok.off.pos.ent"
    return send_file(filename, as_attachment=True)
