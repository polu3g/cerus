
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/faiss_index")
    DEFAULT_PROMPT_PATH = os.getenv("DEFAULT_PROMPT_PATH", "./app/prompts")

settings = Settings()
