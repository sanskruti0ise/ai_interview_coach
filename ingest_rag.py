import tempfile
from unstructured.partition.auto import partition
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize embedding model
embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5")  # CPU/GPU compatible

# Initialize ChromaDB client
client = chromadb.Client()
collection = client.get_or_create_collection("ai_interview_coach")

def load_resume(uploaded_file):
    """
    Parse a PDF/DOCX resume uploaded via Streamlit and return extracted text.
    """
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Use unstructured to parse the temp file
    elements = partition(filename=tmp_path)
    text = "\n".join([str(el) for el in elements])

    return text

def load_jd(text):
    """Process job description text (already in string)."""
    return text

def chunk_text(text, chunk_size=500):
    """Split text into chunks for embeddings."""
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def embed_and_store(chunks, source):
    """Create embeddings and store in ChromaDB."""
    for i, chunk in enumerate(chunks):
        embedding = embed_model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            metadatas=[{"source": source, "chunk_id": i}],
            embeddings=[embedding]
        )
