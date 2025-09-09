import tempfile
from pypdf import PdfReader

def load_resume(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text
    elif uploaded_file.name.endswith(".docx"):
        from docx import Document
        doc = Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    else:
        return "Unsupported file format"

def load_jd(text):
    """Process job description text (already in string)."""
    return text

def chunk_text(text, chunk_size=500):
    """Split text into chunks for later use (if needed)."""
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

