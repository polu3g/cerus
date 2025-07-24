import os
import re
import requests
from typing import Dict
from app.services.prompt_loader import load_prompt
from app.vectorstore.faiss_store import similarity_search
from app.core.config import settings
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from trulens_eval import Tru
from trulens_eval import Feedback, tru_chain
from trulens_eval.feedback import GroundTruthAgreement
from trulens.providers.openai import OpenAI as fOpenAI
from trulens.apps.app import instrument
from trulens.core import TruSession

session = TruSession()
session.reset_database()

GEMINI_ENDPOINT = settings.GEMINI_ENDPOINT
print(os.getenv("OPENAI_API_KEY"))
golden_set = [
    {
        "query": "who invented the lightbulb?",
        "expected_response": "Thomas Edison",
    },
    {
        "query": "¿quien invento la bombilla?",
        "expected_response": "Thomas Edison",
    },
]

tru = Tru()

# Optional: Set up TruLens to run a dashboard
tru.run_dashboard()  # Opens dashboard at http://localhost:8501

feedback = Feedback(
    GroundTruthAgreement(golden_set, provider=fOpenAI()).agreement_measure,
    name="Ground Truth Semantic Agreement",
).on_input_output()

@instrument
def call_gemini(prompt: str) -> str:
    """Call Gemini 2.0 API with a prompt and return the generated text"""
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_ENDPOINT, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise ValueError(f"Unexpected response format: {e}")
    else:
        raise RuntimeError(f"Gemini API error {response.status_code}: {response.text}")


def clean_response(text: str) -> str:
    text = text.replace('\n', ' ')
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text

# Step nodes
def load_prompts(state: Dict) -> Dict:
    client_id = state["client_id"]
    return {
        "intent_prompt": load_prompt(client_id, "intent"),
        "infer_prompt": load_prompt(client_id, "infer"),
        **state
    }

def extract_intent(state: Dict) -> Dict:
    intent_prompt = state["intent_prompt"]
    query = state["query"]
    prompt = f"{intent_prompt}\n\nQuery:\n{query}"
    intent = call_gemini(prompt).strip()
    return {**state, "extracted_intent": intent}

def search_similar_docs(state: Dict) -> Dict:
    docs = similarity_search(state["extracted_intent"], k=10)
    context = "\n".join([doc.page_content for doc in docs])
    return {**state, "context": context}

def run_inference(state: Dict) -> Dict:
    infer_prompt = state["infer_prompt"]
    context = state["context"]
    query = state["query"]
    prompt = f"{infer_prompt}\n\nContext:\n{context}\n\nQuery:\n{query}"
    response = call_gemini(prompt)
    return {**state, "raw_response": response}

def finalize(state: Dict) -> Dict:
    return {
        "client_id": state["client_id"],
        "query": state["query"],
        "extracted_intent": state["extracted_intent"],
        "response": clean_response(state["raw_response"]),
        "model_type": "RAG",
        "model_ver": "Cerus v1.0"
    }

# Define the state schema or input/output
state_schema = frozenset({
    "client_id": {"type": "string"},
    "query": {"type": "string"},
    "extracted_intent": {"type": "string"},
    "context": {"type": "string"},
    "raw_response": {"type": "string"}
})

# Build the StateGraph
graph = StateGraph(state_schema=state_schema)

graph.add_node("load_prompts", RunnableLambda(load_prompts))
graph.add_node("extract_intent", RunnableLambda(extract_intent))
graph.add_node("search_similar_docs", RunnableLambda(search_similar_docs))
graph.add_node("run_inference", RunnableLambda(run_inference))
graph.add_node("finalize", RunnableLambda(finalize))

graph.set_entry_point("load_prompts")
graph.add_edge("load_prompts", "extract_intent")
graph.add_edge("extract_intent", "search_similar_docs")
graph.add_edge("search_similar_docs", "run_inference")
graph.add_edge("run_inference", "finalize")

inference_chain = graph.compile()

# Wrapper function
def generate_inference(client_id: str, query: str) -> Dict:
    return inference_chain.invoke({"client_id": client_id, "query": query})
