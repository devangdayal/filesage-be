import os
import datetime
import time
import logging
from typing import Dict, List
from concurrent.futures import ProcessPoolExecutor, as_completed
import pdfplumber
from docx import Document
from app.model.constant import SCANNER_SUPPORTED_EXTENSIONS  



def fetch_file_metadata(file_path: str) -> Dict:
    """
    Extract metadata and a content preview from a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        Dict: Metadata for the file.
    """
    start = time.time()
    try:
        stat = os.stat(file_path)
        created_at = datetime.datetime.fromtimestamp(stat.st_ctime).isoformat()
        modified_at = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        size_bytes = os.path.getsize(file_path)
        size_mb = round(size_bytes / (1024 * 1024), 2)
        extension = os.path.splitext(file_path)[1].lower()
        directory = os.path.dirname(file_path)
        name = os.path.basename(file_path)

        content_preview = ""
        is_readable = False

        if extension == ".pdf":
            try:
                with pdfplumber.open(file_path) as pdf:
                    if pdf.pages:
                        content_preview = (pdf.pages[0].extract_text() or "").strip()[:300]
                        is_readable = bool(content_preview)
            except Exception as e:
                logging.error(f"[ERROR] PDF read failed: {file_path} — {e}")

        elif extension in [".txt", ".md"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content_preview = f.read(1000).strip()
                    is_readable = bool(content_preview)
            except Exception as e:
                logging.error("[ERROR] Text read failed: %s: %s",{file_path},{e})

        elif extension == ".docx":
            try:
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs[:5]])
                content_preview = text.strip()[:500]
                is_readable = bool(content_preview)
            except Exception as e:
                logging.error("[ERROR] DOCX read failed: %s: %s",{file_path},{e})

        return {
            "name": name,
            "path": directory,
            "absolute_path": os.path.abspath(file_path),
            "extension": extension,
            "created_at": created_at,
            "modified_at": modified_at,
            "size": size_mb,
            "content_preview": content_preview,
            "is_readable": is_readable
        }

    except FileNotFoundError as e:
        logging.error("[ERROR] Failed to scan %s: %s",{file_path},{e})
        return {}
    finally:
        logging.info("[TIMER] %s took %s s",{extension},{round(time.time() - start, 2)})


def scan_directory(root_dir: str, extensions: List[str] = None, max_workers: int = 8) -> List[Dict]:
    """
    Recursively scans a directory and returns metadata for supported files.

    Args:
        root_dir (str): Directory path to scan.
        extensions (List[str], optional): File types to include.
        max_workers (int): Number of parallel workers to use.

    Returns:
        List[Dict]: List of file metadata.
    """
    extensions = extensions or SCANNER_SUPPORTED_EXTENSIONS
    file_paths = []
    results = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(dirpath, filename))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(fetch_file_metadata, path): path for path in file_paths}

        for future in as_completed(future_to_path):
            result = future.result()
            if result:
                results.append(result)

    return results
