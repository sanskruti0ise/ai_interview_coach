# core_logic.py
import os
import requests
from dotenv import load_dotenv

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
'''
def generate_questions(resume_text, jd_text):
    prompt = f"Generate 5 targeted interview questions based on the resume and JD:\nResume: {resume_text}\nJD: {jd_text}"
    return call_mistral(prompt)
'''
def generate_questions(resume_text, jd_text=None):
    if jd_text:
        prompt = f"""
        You are an AI Interview Coach. Based on the following resume and job description, 
        generate exactly 10 tailored interview questions that focus on the candidate’s skills, 
        experiences, and potential gaps.

        Resume:
        {resume_text}

        Job Description:
        {jd_text}

        Format as a numbered list (1–10).
        """
    else:
        prompt = f"""
        You are an AI Interview Coach. Based only on the following resume, 
        generate exactly 10 interview questions that the candidate might be asked 
        in a technical and behavioral interview.

        Resume:
        {resume_text}

        Format as a numbered list (1–10).
        """

    return call_mistral(prompt)
