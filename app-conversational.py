# app.py
import streamlit as st
from ingest_rag import load_resume, load_jd  # RAG-enabled ingestion
from core_logic import generate_gap_analysis, generate_questions

st.set_page_config(page_title="AI Interview Coach", layout="wide")

st.title("🤖 AI Interview Coach")
st.markdown("""
Welcome! Upload your resume (PDF/DOCX) and optionally paste a Job Description. 
The AI will generate a gap analysis and 10 targeted interview questions.
""")

# --- Upload Resume ---
resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description (Optional)")

use_rag = st.checkbox("Use RAG for context?", value=True)

if st.button("Generate Questions") and resume_file:
    with st.spinner("Parsing resume and generating questions..."):
        # --- Load Resume ---
        resume_text = load_resume(resume_file)
        jd_text_processed = load_jd(jd_text) if jd_text else None

        # --- Generate Gap Analysis ---
        gap_summary = generate_gap_analysis(resume_text, jd_text_processed, use_rag=use_rag)
        st.subheader("📝 Gap Analysis")
        st.write(gap_summary)

        # --- Generate Interview Questions ---
        questions = generate_questions(resume_text, jd_text_processed, use_rag=use_rag)

        # Clean up numbering if returned as string
        if isinstance(questions, str):
            questions_list = [
                q.lstrip("1234567890. ").strip() 
                for q in questions.split("\n") if q.strip()
            ]
        else:
            questions_list = questions

        st.subheader("💡 Interview Questions")
        for idx, q in enumerate(questions_list, start=1):
            st.write(f"{idx}. {q}")

        st.success("✅ Done! You can now review the gap analysis and practice your answers.")

