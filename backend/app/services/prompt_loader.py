
import os
from app.core.config import settings

def load_prompt(client_id: str, prompt_type: str) -> str:
    fname = f"{client_id}_{prompt_type}_prompt.txt"
    path = os.path.join(settings.DEFAULT_PROMPT_PATH, fname)
    default_path = os.path.join(settings.DEFAULT_PROMPT_PATH, f"default_{prompt_type}_prompt.txt")
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    with open(default_path) as f:
        return f.read()
