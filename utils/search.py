import os
import sqlite3
import faiss
import numpy as np
from utils.logger import logger
from typing import List, Tuple
from utils.embeddings import get_embedding



DB_PATH = 'chat_assistant/data/document_store.db'
FAISS_INDEX_PATH = 'chat_assistant/data/faiss.index'


EMBEDDING_DIM = 1536

def init_faiss_index() -> faiss.IndexFlatL2:
    
    if os.path.exists(FAISS_INDEX_PATH):
        logger.info("[FAISS] Loading existing FAISS index...")
        return faiss.read_index(FAISS_INDEX_PATH)
    else:
        logger.error("[FAISS] No FAISS index found!")
        return None

def search_in_faiss(query: str, faiss_index: faiss.IndexFlatL2, top_k: int = 5) -> List[int]:
    
    embedding = get_embedding(query)
    if embedding:
        np_embedding = np.array([embedding]).astype('float32')  
        distances, indices = faiss_index.search(np_embedding, top_k)
        return indices[0]  
    return []

def search_in_sqlite(query: str) -> List[Tuple[int, str]]:
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = f"%{query}%"  
    c.execute('''
        SELECT id, filename
        FROM documents
        WHERE text LIKE ? OR chunks LIKE ?
    ''', (query, query))
    results = c.fetchall()
    conn.close()
    return results

def full_text_search(query: str, top_k: int = 5) -> List[dict]:
    
    faiss_index = init_faiss_index()
    if faiss_index is None:
        return []

    logger.info(f"[Search] Searching for '{query}'...")

    
    faiss_results = search_in_faiss(query, faiss_index, top_k)


    sqlite_results = search_in_sqlite(query)

  
    results = []
    for idx in faiss_results:
        results.append({"type": "FAISS", "document_id": idx})

    for doc_id, filename in sqlite_results:
        results.append({"type": "SQLite", "document_id": doc_id, "filename": filename})

    return results

