"""Extracting full content from a single supported file."""

import os
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.model.request import PathRequest
from app.utils.chunker import chunk_text, normalize_text
from app.utils.content_extractor import extract_full_content
from app.utils.embedding import generate_embeddings

router = APIRouter()

@router.post("/content-extract-directory")
def extract_content(request: PathRequest):
    """Extract content from a file and generate embeddings."""
    try:
        if not os.path.isfile(request.path):
            return JSONResponse(status_code=404, content={"error": "File not found"})

        raw_text = extract_full_content(file_path=request.path)
        cleaned_text = normalize_text(raw_text)
        chunks = chunk_text(cleaned_text)
        embeddings = generate_embeddings(chunks)

        return {
            "status": "success",
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0] if chunks else "",
            "sample_embedding": embeddings[0] if embeddings else [],
        }

    except Exception as e:
        logging.exception("Unexpected error during content extraction and embedding.")
        return JSONResponse(status_code=500, content={"error": str(e)})

