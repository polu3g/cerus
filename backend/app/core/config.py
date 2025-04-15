
import os
from dotenv import load_dotenv
load_dotenv()

import os

class Settings:
    def __init__(self):
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/faiss_index")
        self.DEFAULT_PROMPT_PATH = os.getenv("DEFAULT_PROMPT_PATH", "./app/prompts")
        self.GEMINI_ENDPOINT = (
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.GOOGLE_API_KEY}"
        )

settings = Settings()
