import os
import json

from flask import Blueprint, current_app, flash, jsonify, render_template, request, redirect, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import db
from .models import Note

views = Blueprint("views", __name__)

# Definition of Homepage
@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/download_file")
@login_required
def download_file():
    filepath = "static/mandelbrot_placeholder.png"  # Path to the file
    return send_file(filepath, as_attachment=True)

@views.route("/download_source")
@login_required
def download_source():
    filepath = "static/mandelbrot_placeholder.py"  # Path to the file
    return send_file(filepath, as_attachment=True)

@views.route("/terms")
def terms():
    with open(os.path.join("docs", "terms_of_service.txt"), "r") as file:
        content = file.readlines()
    return render_template("show_docs.html", content=content, user=current_user)

@views.route("/privacy")
def privacy():
    with open(os.path.join("docs", "privacy_policy.txt"), "r") as file:
        content = file.readlines()
    return render_template("show_docs.html", content=content, user=current_user)

@views.route("/introduction")
def introduction():
    with open(os.path.join("docs", "introduction.txt"), "r") as file:
        content = file.readlines()
    return render_template("show_docs.html", content=content, user=current_user)

@views.route("/about_us")
def about_us():
    with open(os.path.join("docs", "about_us.txt"), "r") as file:
        content = file.readlines()
    return render_template("show_docs.html", content=content, user=current_user)

@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    # Creation of a Note by the user
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short.", category="error")
        else:
            new_note = Note(text=note, user_id=current_user.id)

            db.session.add(new_note)
            db.session.commit()

            flash("Note added.", category="success")

    return render_template("notes.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    # Extracting noteId
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted.", category="success")

    # Returning empty response
    return jsonify({})
