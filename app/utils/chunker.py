import re
from typing import List


def normalize_text(text: str) -> str:
    """
    Clean up the extracted content.
    - Remove excessive newlines, spaces.
    - Fix common formatting issues.
    """
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    
    return text.strip()

def chunk_text(text: str, max_tokens: int = 300) -> List[str]:
    """
    Break text into chunks based on paragraph or sentence boundaries.

    Args:
        text (str): Cleaned text
        max_tokens (int): Max chunk size (approx. in words)

    Returns:
        List[str]: Chunks of text
    """
    paragraphs = re.split(r'\n+', text)
    chunks = []
    current_chunk = []

    current_token_count = 0

    for para in paragraphs:
        tokens = para.strip().split()
        if not tokens:
            continue

        if current_token_count + len(tokens) <= max_tokens:
            current_chunk.append(para.strip())
            current_token_count += len(tokens)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [para.strip()]
            current_token_count = len(tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
