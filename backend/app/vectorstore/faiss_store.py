import os
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
load_dotenv()

DATA_DIR = "./data"
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/faiss_index")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embedding = GoogleGenerativeAIEmbeddings( model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

db = FAISS.load_local(settings.VECTOR_DB_PATH, embeddings=embedding, allow_dangerous_deserialization=True)

def similarity_search(query: str, k: int = 3) -> List:
    return db.similarity_search(query, k=k)
