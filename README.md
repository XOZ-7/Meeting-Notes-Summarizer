# 📝 Meeting Notes Summarizer

A Flask-based web application that automatically summarizes meeting notes using Amazon Bedrock. Users can either paste meeting notes directly into the application or upload a `.txt` file. The application generates an executive summary, extracts action items, identifies key decisions, and highlights open questions using an LLM.

---

## 🚀 Features

- Paste meeting notes directly into the web interface
- Upload `.txt` meeting transcripts
- Executive summary generation
- Action item extraction
- Key decision identification
- Open question detection
- Token usage statistics
- Input validation and error handling
- Clean and responsive user interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Backend
- Python
- Flask

### AI & Cloud
- Amazon Bedrock
- Claude Model
- boto3 (AWS SDK)

---

## 📂 Project Structure

```
Meeting-Notes-Summarizer/
│
├── app.py                  # Flask application
├── config.py               # Configuration settings
├── llm_client.py           # Amazon Bedrock integration
├── prompts.py              # System prompt
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
└── test_samples/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Meeting-Notes-Summarizer.git
cd Meeting-Notes-Summarizer
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`.

Example:

```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION=us-east-1
MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0

FLASK_DEBUG=True
PORT=5000
```

---

## ▶️ Running the Application

```bash
python app.py
```

Open your browser and visit

```
http://localhost:5000
```

---

## 📋 How It Works

1. User enters meeting notes or uploads a `.txt` file.
2. Flask validates the input.
3. The backend sends the meeting notes to Amazon Bedrock.
4. Claude generates a structured response.
5. The application displays:

- Executive Summary
- Action Items
- Key Decisions
- Open Questions
- Token Usage

---

## 📥 Supported Input

✔ Plain text

✔ `.txt` files

Maximum upload size: **5 MB**

Maximum text length: **10,000 characters**

---

## 📤 Example Output

```json
{
  "summary": "The team discussed the upcoming product launch and finalized deployment plans.",

  "action_items": [
    "Rahul: Complete authentication API by Friday",
    "Alice: Begin UI testing after API completion"
  ],

  "key_decisions": [
    "Production release postponed by one week"
  ],

  "open_questions": [
    "Which payment gateway vendor will be selected?"
  ],

  "token_usage": {
    "input": 210,
    "output": 145,
    "total": 355
  }
}
```

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| AWS_ACCESS_KEY_ID | AWS Access Key |
| AWS_SECRET_ACCESS_KEY | AWS Secret Access Key |
| AWS_REGION | AWS Region |
| MODEL_ID | Bedrock Model ID |
| FLASK_DEBUG | Flask Debug Mode |
| PORT | Application Port |

---

## 📦 Dependencies

- Flask
- python-dotenv
- boto3

Install using

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Future Improvements

- PDF and DOCX support
- Meeting transcript speaker identification
- Export summary to PDF
- Authentication
- Meeting history
- Multiple AI model support
- Dark mode

---

## 📄 License

This project is intended for educational and learning purposes.
