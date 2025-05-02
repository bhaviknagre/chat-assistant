import faiss
import numpy as np
import os
import pickle
from utils.logger import logger




DB_PATH = "chat_assistant/data/document_store.db"
FILES_DIR = "chat_assistant/data/files/"
FAISS_INDEX_PATH = "chat_assistant/data/faiss.index"


os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


EMBEDDING_DIM = 1536

def init_faiss_index():
    if os.path.exists(FAISS_INDEX_PATH):
        logger.info("[FAISS] Loading existing FAISS index...")
        index = faiss.read_index(FAISS_INDEX_PATH)
    else:
        logger.info("[FAISS] Creating new FAISS index...")
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
    return index

def save_faiss_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT,
            upload_time TEXT,
            text BLOB,
            chunks BLOB,
            num_chunks INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def store_document(file_path: str, text: str, chunks: List[str], embeddings: List[List[float]]):
    """
    Store file, text, chunks, embeddings, metadata in DB and FAISS.

    Args:
        file_path (str): Path to uploaded file
        text (str): Cleaned full text
        chunks (List[str]): List of text chunks
        embeddings (List[List[float]]): Embedding vectors for chunks
    """
    init_db()
    faiss_index = init_faiss_index()

    filename = os.path.basename(file_path)
    upload_time = datetime.now().isoformat()

  
    new_file_path = os.path.join(FILES_DIR, filename)
    os.replace(file_path, new_file_path)

   
    text_blob = pickle.dumps(text)
    chunks_blob = pickle.dumps(chunks)

 
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO documents (filename, filepath, upload_time, text, chunks, num_chunks)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, new_file_path, upload_time, text_blob, chunks_blob, len(chunks)))
    document_id = c.lastrowid
    conn.commit()
    conn.close()

 
    logger.info(f"[FAISS] Adding {len(embeddings)} embeddings to index...")
    np_embeddings = np.array(embeddings).astype('float32')
    faiss_index.add(np_embeddings)
    save_faiss_index(faiss_index)

    logger.info(f"[Storage] Document '{filename}' stored with ID {document_id}.")


