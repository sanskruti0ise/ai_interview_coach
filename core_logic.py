import os
import requests
from dotenv import load_dotenv
from ingest import chunk_text, embed_and_store, collection

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def call_mistral(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-small",  # or mistral-medium/large depending on your key
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def generate_gap_analysis(resume_text, jd_text):
    prompt = f"Analyze the resume vs JD:\nResume: {resume_text}\nJD: {jd_text}\nProvide a gap analysis summary."
    return call_mistral(prompt)

def generate_questions(resume_text, jd_text=None):
    # Step 1: Clear and re-ingest data
    resume_chunks = chunk_text(resume_text)
    embed_and_store(resume_chunks, source="resume")

    if jd_text:
        jd_chunks = chunk_text(jd_text)
        embed_and_store(jd_chunks, source="jd")

    # Step 2: Query vector DB for relevant chunks
    query = "Generate tailored interview questions"
    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    retrieved_context = "\n".join(results["documents"][0])

    # Step 3: Build RAG prompt
    if jd_text:
        prompt = f"""
        You are an AI Interview Coach. Based on the candidate’s resume and job description,
        generate exactly 10 tailored interview questions that focus on technical depth,
        project experience, and gaps.

        Retrieved Context:
        {retrieved_context}

        Format as a numbered list (1–10).
        """
    else:
        prompt = f"""
        You are an AI Interview Coach. Based only on the candidate’s resume,
        generate exactly 10 tailored interview questions focusing on technical
        and behavioral aspects.

        Retrieved Context:
        {retrieved_context}

        Format as a numbered list (1–10).
        """

    return call_mistral(prompt)
