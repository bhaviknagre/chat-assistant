import os
import fitz 
import docx
from utils.logger import logger


def extract_text_from_pdf(file_path):
    
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        logger.info(f"[PDF Extraction] Successfully extracted text from {file_path}")
    except Exception as e:
        logger.error(f"[PDF Extraction] Failed to extract PDF text: {e}")
        raise
    return text


def extract_text_from_docx(file_path):
    
    text = ""
    try:
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        logger.info(f"[DOCX Extraction] Successfully extracted text from {file_path}")
    except Exception as e:
        logger.error(f"[DOCX Extraction] Failed to extract DOCX text: {e}")
        raise
    return text


def extract_text_from_txt(file_path):
    
    text = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        logger.info(f"[TXT Extraction] Successfully extracted text from {file_path}")
    except Exception as e:
        logger.error(f"[TXT Extraction] Failed to extract TXT text: {e}")
        raise
    return text


def extract_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported types are PDF, DOCX, TXT")

