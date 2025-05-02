import logging
from utils import file_extraction, chunks, embeddings, storehouse
from utils.logger import logger


def run_pipeline(file_path: str):
   
    logger.info(f"[Pipeline] Starting pipeline for file: {file_path}")

   
    text = file_extraction.extract_text(file_path)
    if not text:
        logger.error("[Pipeline] No text extracted. Aborting pipeline.")
        return
    logger.info(f"[Pipeline] Text extraction complete. Length: {len(text)} characters")

    text_chunks = chunks.chunk_text(text)
    logger.info(f"[Pipeline] Text chunking complete. {len(text_chunks)} chunks created.")

    
    embeddings = embedding.embed_chunks(text_chunks)
    logger.info(f"[Pipeline] Embedding complete. {len(embeddings)} embeddings generated.")

    
    storhouse.store_document(file_path, text, text_chunks, embeddings)
    logger.info(f"[Pipeline] Document stored successfully.")

    logger.info("[Pipeline] Pipeline execution finished.\n")

