# coach.py
from core_logic import call_mistral

def evaluate_answer(question, user_answer):
    prompt = f"Question: {question}\nUser Answer: {user_answer}\nEvaluate this answer and provide constructive feedback."
    return call_mistral(prompt)

def get_model_answer(question):
    prompt = f"Question: {question}\nProvide an ideal model answer."
    return call_mistral(prompt)

