from utils.document_loader import load_document
from utils.chunks import split_loaded_document
from utils.embedding_generator import embed_documents
from utils.store_house import store_document
from utils.logger import logger


def run_pipeline(file_path: str):
    logger.info(f"[Pipeline] Starting pipeline for file: {file_path}")

    # 1. Load document and extract content
    try:
        documents = load_document(file_path)
        logger.info(f"[Pipeline] Loaded {len(documents)} document(s).")
    except Exception as e:
        logger.error(f"[Pipeline] Document loading failed: {e}")
        return

    # 2. Chunk the document
    try:
        chunks = split_loaded_document(file_path)
        logger.info(f"[Pipeline] Document chunking complete. {len(chunks)} chunks created.")
    except Exception as e:
        logger.error(f"[Pipeline] Chunking failed: {e}")
        return

    # 3. Generate embeddings
    try:
        generated_embeddings = embed_documents(chunks)
        logger.info(f"[Pipeline] Embedding complete. {len(generated_embeddings)} embeddings generated.")
    except Exception as e:
        logger.error(f"[Pipeline] Embedding failed: {e}")
        return

    # 4. Store in Chroma
    try:
        raw_text = "\n".join([doc.page_content for doc in documents])
        store_document(file_path, raw_text, chunks, generated_embeddings)
        logger.info(f"[Pipeline] Document stored successfully.")
    except Exception as e:
        logger.error(f"[Pipeline] Storing failed: {e}")
        return

    logger.info("[Pipeline] Pipeline execution finished.\n")
