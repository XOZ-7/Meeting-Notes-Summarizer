"""
Meeting Notes Summarizer - Flask Backend
------------------------------------------
Handles Flask routes, request validation, and returns structured JSON responses.
Delegates model inference cleanly to `llm_client.py`.
"""

import os
from flask import Flask, render_template, request, jsonify
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, MAX_CHARACTERS, FLASK_DEBUG, PORT
from llm_client import generate_summary

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_BYTES + (1 * 1024 * 1024)  # Buffer for form overhead


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has a permitted extension (.txt)."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Serve the main interface."""
    return render_template("index.html", max_characters=MAX_CHARACTERS)


@app.route("/generate", methods=["POST"])
def generate():
    """
    Accepts meeting notes via form text or .txt file upload and delegates 
    to llm_client.generate_summary().
    """
    notes_text = (request.form.get("notes") or "").strip()
    uploaded_file = request.files.get("file")

    has_text = bool(notes_text)
    has_file = uploaded_file is not None and uploaded_file.filename != ""

    if not has_text and not has_file:
        return jsonify({"error": "Please paste meeting notes or upload a .txt file."}), 400

    final_text = notes_text

    if has_file:
        if not allowed_file(uploaded_file.filename):
            return jsonify({"error": "Only .txt files are supported."}), 400

        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        if file_size > MAX_FILE_SIZE_BYTES:
            return jsonify({"error": "File exceeds the maximum size of 5MB."}), 400

        try:
            final_text = uploaded_file.read().decode("utf-8", errors="replace")
        except Exception:
            return jsonify({"error": "Could not read the uploaded file. Please upload a valid .txt file."}), 400

    if not final_text or not final_text.strip():
        return jsonify({"error": "The provided notes are empty."}), 400

    if len(final_text) > MAX_CHARACTERS:
        return jsonify({"error": f"Notes exceed the maximum of {MAX_CHARACTERS} characters."}), 400

    result = generate_summary(final_text)
    return jsonify(result), 200


@app.errorhandler(413)
def file_too_large(_e):
    return jsonify({"error": "File exceeds the maximum size of 5MB."}), 413


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, port=PORT)