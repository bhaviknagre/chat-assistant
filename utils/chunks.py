from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List 
from utils.document_loader import load_document
from utils.logger import logger
import tiktoken


def tiktoken_len(text: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return len(tokenizer.encode(text))


def split_loaded_document(file_path: str, chunk_size: int = 500, overlap: int = 50) -> List[Document]:
    documents = load_document(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""],  
        length_function=tiktoken_len
    )

    all_chunks = []

    for doc in documents:
        if not doc.page_content.strip():
            continue  

        text_chunks = splitter.split_text(doc.page_content)
        logger.info(f"[Chunking] File: {doc.metadata.get('source', 'unknown')} → {len(text_chunks)} chunks")

        for i, chunk in enumerate(text_chunks):
            chunk_doc = Document(
                page_content=chunk,
                metadata={
                    **doc.metadata,
                    "chunk": i + 1,
                    "total_chunks": len(text_chunks)
                }
            )
            all_chunks.append(chunk_doc)

    logger.info(f"[Chunking] Split {len(documents)} documents into {len(all_chunks)} chunks total")
    return all_chunks
