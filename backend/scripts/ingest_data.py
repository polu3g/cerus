
import os
import re
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from dotenv import load_dotenv
from PIL import Image
import pytesseract
from langchain_core.documents import Document

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
            docs.extend(loader.load())
        elif fname.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif fname.endswith(".png"):
            try:
                text = pytesseract.image_to_string(Image.open(path))
                text = text.replace('\n', ' ').strip()  # Remove newlines and trim whitespace
                text = re.sub(r'\s+', ' ', text).strip() 
                if text:
                    docs.append(Document(page_content=text, metadata={"source": fname}))
            except Exception as e:
                print(f"Error processing image {fname}: {e}")
       
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
