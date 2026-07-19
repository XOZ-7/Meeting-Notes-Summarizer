# Meeting Notes Summarizer

A fully working frontend + backend prototype for a meeting-notes summarization
tool. The AI model is **not yet integrated** — the backend currently returns
hardcoded placeholder data so the entire product can be built, tested, and
demoed end-to-end before any AI dependency exists.

## Tech stack

- Python 3.11+
- Flask
- HTML5 / CSS3 / Vanilla JavaScript (no frontend framework, no build step)
- python-dotenv for environment variables

## Project structure

```
meeting-summarizer/
├── app.py               Flask app: routes, validation, placeholder response
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── templates/
│   └── index.html       Main UI
├── static/
│   ├── style.css
│   └── script.js
└── uploads/              (unused for persistence — files are read in-memory)
```

## Setup

```bash
cd meeting-summarizer
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Then open **http://localhost:5000** in your browser.

## How it works today

1. User pastes text or uploads a `.txt` file in the UI.
2. Frontend sends it to `POST /generate` via `fetch()` (no page reload).
3. Backend validates the input (empty check, file type, file size, character
   limit) and returns a **hardcoded** JSON payload from
   `generate_summary_placeholder()` in `app.py`.
4. Frontend renders the response into the five result cards.

No AI provider, API key, or network call to any model is used anywhere in
this codebase yet.

## Plugging in real AI later

Everything is intentionally isolated so that adding AWS Bedrock (GPT-OSS-20B)
or another provider requires editing **one function**:

```python
# app.py
def generate_summary_placeholder(meeting_notes_text: str) -> dict:
    ...
```

Replace its body with a real model call, keeping the same return shape:

```python
{
  "summary": str,
  "action_items": list[str],
  "key_decisions": list[str],
  "open_questions": list[str],
  "token_usage": {"input": int, "output": int, "total": int}
}
```

No other file needs to change — the route, validation, and the entire
frontend already expect exactly this contract.

## Notes

- Uploaded files are read directly from the in-memory request stream; they
  are **not** written to disk or persisted (`uploads/` exists for future use
  only).
- Max upload size: 5MB. Max pasted text: 10,000 characters.
- Only `.txt` files are accepted.
