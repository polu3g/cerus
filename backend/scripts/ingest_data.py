
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "./data/data"
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/faiss_index")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embedding = GoogleGenerativeAIEmbeddings( model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

def load_documents():
    docs = []
    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)
        if fname.endswith(".txt"):
            loader = TextLoader(path)
        elif fname.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            continue
        docs.extend(loader.load())
    return docs

def main():
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")
    print("Creating vector index...")
    db = FAISS.from_documents(documents, embedding)
    db.save_local(VECTOR_DB_PATH)
    print(f"Index saved to {VECTOR_DB_PATH}")

if __name__ == "__main__":
    main()
