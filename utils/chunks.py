import re 
from utils.logger import logger


def split_text(text, chunk_size=500, overlap=50):
    
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")

    logger.info("[Text Chunking] Splitting text into chunks...")


    words = re.findall(r'\S+', text)
    total_words = len(words)

    chunks = []
    start = 0

    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)

        
        start += chunk_size - overlap

    logger.info(f"[Text Chunking] Split into {len(chunks)} chunks.")
    return chunks


