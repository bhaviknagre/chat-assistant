import re
from utils.logger import logger
import openai
from typing import List

openai.api_key = "OPENAI_API_KEY"


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    
    try:
        response = openai.Embedding.create(
            input=text,
            model=model
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        logger.error(f"[Embedding] Failed to embed text chunk: {e}")
        return []


def embed_chunks(chunks: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:

    logger.info(f"[Embedding] Embedding {len(chunks)} text chunks...")
    embeddings = []

    for chunk in tqdm(chunks, desc="Embedding chunks"):
        embedding = get_embedding(chunk, model=model)
        embeddings.append(embedding)

    logger.info("[Embedding] Embedding completed.")
    return embeddings


