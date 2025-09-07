import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
