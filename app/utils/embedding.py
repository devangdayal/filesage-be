from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for list of text chunks using sentence-transformers.
    Returns a list of vector embeddings (floats).
    """
    return model.encode(chunks, convert_to_numpy=True).tolist()
