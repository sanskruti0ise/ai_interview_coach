import streamlit as st
from ingest import load_resume, chunk_text
from core_logic import generate_gap_analysis, generate_questions

# Page Config
st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide"
)

st.title("🤖 AI Interview Coach")

# Step 1: Resume Upload
st.header("Step 1: Upload Resume (PDF or DOCX)")
resume_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

# Step 2: Job Description Input (Optional)
st.header("Step 2: Enter Job Description (Optional)")
jd_text = st.text_area("Paste the job description here (optional):", height=200)

# Step 3: Generate Button
if st.button("Generate Questions & Analysis"):

    if not resume_file:
        st.warning("Please upload a resume file.")
    else:
        with st.spinner("Processing..."):

            # --- Load Resume ---
            resume_text = load_resume(resume_file)

            # --- Chunk Text ---
            resume_chunks = chunk_text(resume_text)
            st.subheader("📄 Chunked Resume")
            for i, chunk in enumerate(resume_chunks):
                st.text_area(f"Chunk {i+1}", chunk, height=100)

            # --- Chunk Job Description (if provided) ---
            if jd_text.strip():
                jd_chunks = chunk_text(jd_text)
                st.subheader("📄 Chunked Job Description")
                for i, chunk in enumerate(jd_chunks):
                    st.text_area(f"Chunk {i+1}", chunk, height=100)
            else:
                jd_text = None

            # --- Gap Analysis (only if JD provided) ---
            if jd_text:
                st.subheader("🔍 Gap Analysis")
                gap_summary = generate_gap_analysis(resume_text, jd_text)
                st.success(gap_summary)
            else:
                st.info("Job description not provided. Skipping gap analysis.")

            # --- Generated Questions ---
            st.subheader("Interview Questions:")
           questions = generate_questions(resume_text, jd_text or "")
           if isinstance(questions, str):
            # Clean up numbering/dots the model adds
            formatted = "\n".join([f"- {q.lstrip('1234567890. ').strip()}" for q in questions.split("\n") if q.strip()])
    st.markdown(formatted)
            else:
                questions_list = questions

            for idx, q in enumerate(questions_list, start=1):
                st.write(f"{idx}. {q}")

