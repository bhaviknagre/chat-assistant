import re
from utils.logger import logger
import unicodedata


def clean_text(text):
    
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")

    logger.info("[Text Preprocessing] Cleaning text...")


    text = unicodedata.normalize("NFKC", text)


    text = "".join(ch for ch in text if ch.isprintable())

    text = re.sub(r"[ \t]+", " ", text)           
    text = re.sub(r"\n\s*\n", "\n", text)          
    text = re.sub(r"\s*\n\s*", "\n", text)         

    
    text = text.strip()

    logger.info("[Text Preprocessing] Cleaning complete.")
    return text

