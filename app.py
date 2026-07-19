"""
Meeting Notes Summarizer - Flask Backend
------------------------------------------
This is a fully working prototype backend. Every route, validation rule,
and response shape is final -- the ONLY missing piece is the actual AI
call, which is isolated inside `generate_summary_placeholder()`.

To wire up a real model later (AWS Bedrock / OpenAI GPT-OSS-20B / etc.):
    1. Open this file.
    2. Replace the body of `generate_summary_placeholder()` with a real
       call to your model provider.
    3. Make sure the function still returns a dict shaped exactly like
       the placeholder response below.
That is the only change required anywhere in the codebase.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"txt"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
MAX_CHARACTERS = 10000

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_BYTES + (1 * 1024 * 1024)  # small buffer for form overhead

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Only .txt files are accepted."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# THE ONLY FUNCTION THAT NEEDS TO CHANGE WHEN AI IS INTRODUCED
# ---------------------------------------------------------------------------
def generate_summary_placeholder(meeting_notes_text: str) -> dict:
    """
    Placeholder for the future AI integration (AWS Bedrock / GPT-OSS-20B).

    Currently returns hardcoded, deterministic placeholder data so the
    frontend can be built and tested end-to-end without any AI dependency.

    Args:
        meeting_notes_text: The raw meeting notes (from textarea or .txt file).

    Returns:
        dict shaped exactly like the final AI response contract.
    """
    return {
        "summary": "This is a placeholder summary.",
        "action_items": [
            "Placeholder Action Item 1",
            "Placeholder Action Item 2",
        ],
        "key_decisions": [
            "Placeholder Decision",
        ],
        "open_questions": [
            "Placeholder Question",
        ],
        "token_usage": {
            "input": 124,
            "output": 42,
            "total": 166,
        },
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the main interface."""
    return render_template("index.html", max_characters=MAX_CHARACTERS)


@app.route("/generate", methods=["POST"])
def generate():
    """
    Accepts either:
      - form field 'notes' (pasted text), OR
      - uploaded file field 'file' (.txt)

    Returns placeholder summary JSON, or a JSON error with an
    appropriate HTTP status code.
    """
    notes_text = (request.form.get("notes") or "").strip()
    uploaded_file = request.files.get("file")

    has_text = bool(notes_text)
    has_file = uploaded_file is not None and uploaded_file.filename != ""

    # Neither text nor file provided
    if not has_text and not has_file:
        return jsonify({"error": "Please paste meeting notes or upload a .txt file."}), 400

    final_text = notes_text

    if has_file:
        if not allowed_file(uploaded_file.filename):
            return jsonify({"error": "Only .txt files are supported."}), 400

        # Validate file size (Flask also enforces MAX_CONTENT_LENGTH globally)
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

    result = generate_summary_placeholder(final_text)
    return jsonify(result), 200


@app.errorhandler(413)
def file_too_large(_e):
    return jsonify({"error": "File exceeds the maximum size of 5MB."}), 413


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, port=int(os.getenv("PORT", 5000)))
