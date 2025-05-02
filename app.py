import streamlit as st
import os
import sqlite3
from utils.file_extraction import extract_text
from utils.chunks import split_text
from utils.embeddings import get_embedding
import numpy as np
import faiss
from utils.logger import logger

# Constants
UPLOAD_FOLDER = "chat_assistant/data/files"
DB_PATH = 'chat_assistant/data/document_store.db'
FAISS_INDEX_PATH = 'chat_assistant/data/faiss.index'
EMBEDDING_DIM = 1536

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit page config
st.set_page_config(page_title="Document Text Extractor & Indexer", layout="wide")
st.title("📄 Document Text Extractor & Indexer")
st.write("Upload a **PDF**, **DOCX**, or **TXT** file to extract text and index it for search.")

# Initialize SQLite DB (create table if not exists)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            text TEXT,
            chunks TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize FAISS index (load existing or create new)
def init_faiss_index():
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            index = faiss.read_index(FAISS_INDEX_PATH)
            logger.info("[FAISS] Loaded existing FAISS index")
            return index
        except Exception as e:
            logger.error(f"[FAISS] Failed to load FAISS index: {e}")
    # Create a new index if it doesn't exist or fails to load
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    logger.info("[FAISS] Created new FAISS index")
    return index

# Save document and chunks into SQLite
def save_to_db(filename, full_text, chunks):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO documents (filename, text, chunks) VALUES (?, ?, ?)',
              (filename, full_text, '\n\n'.join(chunks)))
    conn.commit()
    conn.close()

# Save FAISS index to disk
def save_faiss_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)
    logger.info("[FAISS] Saved FAISS index to disk")

# Upload widget
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Save file locally
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File saved to `{file_path}`")

    # Initialize DB
    init_db()

    # Extract text
    try:
        extracted_text = extract_text(file_path)
        st.subheader("📄 Extracted Text")
        st.text_area("Extracted text:", extracted_text, height=400)

        # Split text into chunks
        chunks = split_text(extracted_text, chunk_size=1000)
        st.subheader("📝 Split into Chunks")
        st.write(f"Total chunks: {len(chunks)}")
        for idx, chunk in enumerate(chunks[:3]):  # Show only first 3 chunks for preview
            st.text_area(f"Chunk {idx+1}", chunk, height=150)

        # Save text & chunks to database
        save_to_db(uploaded_file.name, extracted_text, chunks)
        st.success("📂 Saved document and chunks to database")

        # Initialize FAISS index and add embeddings
        faiss_index = init_faiss_index()

        embeddings = []
        for chunk in chunks:
            embedding = get_embedding(chunk)
            if embedding:
                embeddings.append(embedding)

        if embeddings:
            np_embeddings = np.array(embeddings).astype('float32')
            faiss_index.add(np_embeddings)
            save_faiss_index(faiss_index)
            st.success(f"📈 Added {len(embeddings)} chunk embeddings to FAISS index")
        else:
            st.warning("⚠️ No embeddings generated. Check if your embedding function works properly.")

        # Download extracted text option
        st.download_button(
            label="💾 Download Extracted Text",
            data=extracted_text,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_extracted.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
