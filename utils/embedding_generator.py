import os
import time
from typing import List, Dict, Any
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
from langchain.docstore.document import Document
from utils.logger import logger

# Load environment variables and initialize client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")

client = OpenAI(api_key=api_key)

MAX_TOKENS = 8191

def embed_documents(documents: List[Document], model: str = "text-embedding-ada-002", batch_size: int = 10) -> List[Dict[str, Any]]:
    logger.info(f"[Embedding] Embedding {len(documents)} chunks in batches of {batch_size}...")

    embeddings = []
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]

    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding Chunks"):
        batch_texts = texts[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]

        try:
            response = client.embeddings.create(
                input=batch_texts,
                model=model
            )
            for embedding_data, text, metadata in zip(response.data, batch_texts, batch_metadatas):
                embeddings.append({
                    "embedding": embedding_data.embedding,
                    "text": text,
                    "metadata": metadata
                })
        except Exception as e:
            logger.error(f"[Embedding] Error on batch {i}-{i + batch_size}: {e}")
            time.sleep(2)
            continue

    logger.info(f"[Embedding] Completed. Total embeddings: {len(embeddings)}")
    return embeddings
