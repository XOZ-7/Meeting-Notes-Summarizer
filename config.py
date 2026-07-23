import os
from dotenv import load_dotenv

load_dotenv()

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"txt"}

# Validation limits
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
MAX_CHARACTERS = 10000

# Future LLM configuration parameters
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-haiku-4-5-20251001-v1:0")

# Application Settings
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
PORT = int(os.getenv("PORT", 5000))

# Ensure upload directory exists on boot
os.makedirs(UPLOAD_FOLDER, exist_ok=True)