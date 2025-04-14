import os
import requests
from app.services.prompt_loader import load_prompt
from app.vectorstore.faiss_store import similarity_search
from app.core.config import settings

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GOOGLE_API_KEY}"
)

def call_gemini(prompt: str) -> str:
    """Call Gemini 2.0 API with a prompt and return the generated text"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(
        GEMINI_ENDPOINT, json=payload, headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise ValueError(f"Unexpected response format: {e}")
    else:
        raise RuntimeError(f"Gemini API error {response.status_code}: {response.text}")


def generate_inference(client_id: str, query: str) -> dict:
    # Step 1: Load prompt templates
    intent_prompt = load_prompt(client_id, "intent")
    infer_prompt = load_prompt(client_id, "infer")

    # Step 2: Extract Intent from user query
    intent_extraction_prompt = f"{intent_prompt}\n\nQuery:\n{query}"
    extracted_intent = call_gemini(intent_extraction_prompt).strip()
    print(f"Extracted Intent: {extracted_intent}")

    # Step 3: Perform similarity search using extracted intent
    similar_docs = similarity_search(extracted_intent)
    context = "\n".join([doc.page_content for doc in similar_docs])

    # Step 4: Prepare final inference prompt using full context and query
    final_prompt = (
        f"{infer_prompt}\n\nContext:\n{context}\n\nQuery:\n{query}"
    )

    # Step 5: Get final response from Gemini
    response = call_gemini(final_prompt)

    return {
        "client_id": client_id,
        "query": query,
        "extracted_intent": extracted_intent,
        "response": response
    }
