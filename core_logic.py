# core_logic.py
import os
import requests
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Initialize embedding model
embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5")  # CPU/GPU compatible

# Initialize ChromaDB client
client = chromadb.Client()
collection = client.get_or_create_collection("ai_interview_coach")

def call_mistral(prompt, temperature=0.2):
    """
    Calls Mistral API with low temperature for factual responses.
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def retrieve_context(query, top_k=5):
    """
    Retrieves the most relevant chunks from ChromaDB based on query.
    """
    query_embedding = embed_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    # Flatten the documents from results
    context = " ".join([doc for docs in results['documents'] for doc in docs])
    return context


def generate_gap_analysis(resume_text, jd_text=None):
    """
    Generate a factual gap analysis using RAG.
    """
    query = f"Analyze the resume vs JD and provide a concise gap analysis."
    if jd_text:
        combined_text = resume_text + "\n" + jd_text
    else:
        combined_text = resume_text

    context = retrieve_context(combined_text)
    prompt = f"Context: {context}\n\nTask: {query}"
    return call_mistral(prompt)


def generate_questions(resume_text, jd_text=None, n_questions=10):
    """
    Generate factual interview questions using RAG.
    """
    query = f"Generate exactly {n_questions} interview questions based on the context."
    combined_text = resume_text
    if jd_text:
        combined_text += "\n" + jd_text

    context = retrieve_context(combined_text)
    prompt = f"Context: {context}\n\nTask: {query}\nFormat as a numbered list."
    return call_mistral(prompt)
