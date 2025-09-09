# AI Interview Coach (Phase 2 - Conversational + RAG)

![AI Interview Coach](https://img.shields.io/badge/AI-Interview%20Coach-blue)

A conversational AI-powered tool to help job candidates prepare for interviews.  
This Phase 2 version integrates **RAG (Retrieval-Augmented Generation)** for context-aware questions and provides **behind-the-scenes transparency**.

---

## 🚀 Features

- **Resume & Job Description Support**: Upload PDF/DOCX resumes and optionally provide a Job Description.  
- **Gap Analysis**: Compare candidate resume vs JD and highlight skill/experience gaps.  
- **Interview Questions**: Generate 10 tailored interview questions based on resume + JD.  
- **RAG Context Retrieval**: Use ChromaDB to find relevant chunks from the resume to enhance question relevance.  
- **Conversational Flow**: Separate buttons for gap analysis and question generation.  
- **Behind-the-Scenes**: View extracted text, AI prompts, context, and raw outputs.  
- **Cloud-Ready**: Works with Mistral API for LLM inference.  

---

## 🧰 Tech Stack

- Python 3.10+  
- [Streamlit](https://streamlit.io/) - Frontend  
- [ChromaDB](https://www.trychroma.com/) - RAG backend  
- [Unstructured](https://github.com/Unstructured-IO/unstructured) - PDF/DOCX parsing  
- [SentenceTransformers](https://www.sbert.net/) - Embeddings  
- [Mistral API](https://mistral.ai/) - LLM inference  
- Optional GPU support for embeddings

---

## 📂 Project Structure

```
ai_interview_coach/
├─ app-conversational.py   # Main conversational Streamlit app
├─ core_logic.py           # AI prompt handling & RAG logic
├─ ingest.py               # Basic resume ingestion (Phase 1)
├─ ingest_rag.py           # RAG-enabled ingestion
├─ coach.py                # (Future) answer evaluation / coaching loop
├─ requirements.txt
├─ README.md
└─ venv/
```

---

## ⚡ Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ai_interview_coach.git
cd ai_interview_coach
```

2. **Create virtual environment & install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Set up Mistral API key**

Create a `.env` file in the root directory:

```
MISTRAL_API_KEY=your_api_key_here
```

4. **Run the app**

```bash
streamlit run app-conversational.py
```

---

## 🎛 Usage

1. Upload your resume (PDF/DOCX).  
2. Optionally paste a job description.  
3. Use **Analyze Gap** to see a gap analysis.  
4. Use **Generate Questions** to get 10 tailored interview questions.  
5. Check **Show Behind-the-Scenes** to view extracted text, context, and raw AI prompts.  

---

## 🔮 Future Phases

- Phase 3: **Coaching Loop** – User submits answers and receives AI feedback.  
- Phase 4: **Deployment & UX polish** – Hosting, error handling, and user experience improvements.  

---

## 📄 License

MIT License © 2025 Sanskruti Ise

---

## 🌐 Demo

Hosted on Streamlit Cloud: [AI Interview Coach](https://aiinterviewcoach-gsmrjxfbvrkfetfgw5cnuf.streamlit.app/)