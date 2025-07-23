"""Module to extract full text content from supported file types."""

import logging
import os
from shutil import ReadError
from venv import logger
import pdfplumber
from docx import Document


def extract_full_content(file_path: str) -> str:
    """
    Extract full content from supported file types.

    Args:
        file_path (str): Absolute path to the file.

    Returns:
        str: Full extracted content as a string.
    """

    extension = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if extension == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    
        elif extension in [".txt",".md"]:
            with open(file_path,"r",encoding="utf-8",errors="ignore") as f:
                text = f.read()
        
        elif extension == ".docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

    except ReadError as e:
        logging.error("Failed to extract content from %s : %s",{file_path},{e});
    
    return text.strip()
