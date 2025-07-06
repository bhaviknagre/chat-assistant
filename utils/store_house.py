import os
from typing import List, Dict, Any
from chromadb import PersistentClient
from utils.logger import logger

PERSIST_DIR = "chroma_store"
COLLECTION_NAME = "legal_documents"

# Initialize persistent client
client = PersistentClient(path=PERSIST_DIR)

def store_document(file_path: str, raw_text: str, chunks: List[Any], embeddings: List[Dict[str, Any]]) -> None:
    try:
        logger.info(f"[Chroma Store] Storing document from: {file_path}")
        
        # Create or get collection
        collection = client.get_or_create_collection(name=COLLECTION_NAME)

        ids = []
        documents = []
        metadatas = []
        embeddings_list = []

        for i, entry in enumerate(embeddings):
            ids.append(f"{os.path.basename(file_path)}_{i}")
            documents.append(entry["text"])
            metadatas.append(entry["metadata"])
            embeddings_list.append(entry["embedding"])

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings_list
        )

        logger.info(f"[Chroma Store] Stored {len(ids)} items in collection '{COLLECTION_NAME}'")

    except Exception as e:
        logger.error(f"[Chroma Store] Failed to store document: {e}")
        raise
