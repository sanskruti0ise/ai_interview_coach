# app_rag.py
import streamlit as st
from ingest_rag import load_resume, load_jd, chunk_text, embed_and_store
from core_logic import generate_gap_analysis, generate_questions, retrieve_context

st.set_page_config(page_title="AI Interview Coach (Phase 2)", layout="wide")
st.title("🧠 AI Interview Coach (RAG-Powered)")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description (optional)", height=200)

if uploaded_file:
    resume_text = load_resume(uploaded_file)
    st.success("✅ Resume loaded successfully!")

    # Store chunks in vector DB (RAG)
    chunks = chunk_text(resume_text)
    embed_and_store(chunks, source=uploaded_file.name)

    # Initialize session state
    if "gap_analysis" not in st.session_state:
        st.session_state.gap_analysis = None
    if "questions" not in st.session_state:
        st.session_state.questions = None

    st.subheader("Select an Action")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 Generate Gap Analysis"):
            with st.spinner("Analyzing resume vs JD..."):
                st.session_state.gap_analysis = generate_gap_analysis(resume_text, jd_text)
                # Retrieve RAG context
                st.session_state.gap_context = retrieve_context(resume_text + "\n" + (jd_text or ""))

    with col2:
        if st.button("💡 Generate Interview Questions"):
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(resume_text, jd_text)
                # Retrieve RAG context
                st.session_state.q_context = retrieve_context(resume_text + "\n" + (jd_text or ""))

    # Display Gap Analysis
    if st.session_state.gap_analysis:
        st.subheader("📝 Gap Analysis")
        st.markdown(st.session_state.gap_analysis)
        if "gap_context" in st.session_state:
            with st.expander("Show Behind-the-Scenes RAG Context"):
                st.text(st.session_state.gap_context)

    # Display Interview Questions
    if st.session_state.questions:
        st.subheader("💡 Interview Questions")
        questions = st.session_state.questions
        if isinstance(questions, str):
            formatted = "\n".join([
                f"- {q.lstrip('1234567890. ').strip()}"
                for q in questions.split("\n") if q.strip()
            ])
            st.markdown(formatted)
        else:
            for idx, q in enumerate(questions, start=1):
                st.write(f"{idx}. {q}")
        if "q_context" in st.session_state:
            with st.expander("Show Behind-the-Scenes RAG Context"):
                st.text(st.session_state.q_context)
