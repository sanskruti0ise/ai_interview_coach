# core_logic.py
import os
import requests
from dotenv import load_dotenv
from ingest_rag import embed_model, collection  # Use the RAG-enabled ingest

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def call_mistral(prompt):
    """
    Calls the Mistral API with a prompt and returns the response text.
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-small",  # or medium/large if your key allows
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


def retrieve_context(query_text, top_k=3):
    """
    Query ChromaDB using embeddings from the resume text (or JD).
    Returns top-k relevant text chunks as context.
    """
    embedding = embed_model.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=top_k,
    )
    # Flatten results into a single string
    context = "\n".join(results['documents'][0])
    return context


def generate_gap_analysis(resume_text, jd_text=None, use_rag=False):
    """
    Generate a Resume-to-JD gap analysis.
    If use_rag=True, it retrieves relevant context from the DB.
    """
    context = resume_text
    if jd_text:
        context += f"\nJob Description:\n{jd_text}"

    if use_rag:
        context = retrieve_context(resume_text)
        if jd_text:
            context += f"\nJob Description:\n{jd_text}"

    prompt = f"""
    You are an AI Interview Coach. Analyze the resume vs JD and provide a clear 
    gap analysis summary.

    Context:
    {context}
    """
    return call_mistral(prompt)


def generate_questions(resume_text, jd_text=None, use_rag=False):
    """
    Generate 10 targeted interview questions based on resume and JD.
    If use_rag=True, uses retrieved context from ChromaDB.
    """
    context = resume_text
    if jd_text:
        context += f"\nJob Description:\n{jd_text}"

    if use_rag:
        context = retrieve_context(resume_text)
        if jd_text:
            context += f"\nJob Description:\n{jd_text}"

    prompt = f"""
    You are an AI Interview Coach. Based on the following context, 
    generate exactly 10 tailored interview questions focusing on skills, 
    experience, and potential gaps.

    Context:
    {context}

    Format as a numbered list (1–10).
    """
    return call_mistral(prompt)
