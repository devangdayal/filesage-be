"""Module for scanning directories and extracting metadata from supported files."""
import os
import datetime
from typing import Dict, List
import pdfplumber




SUPPORTED_EXTENSIONS = [".pdf", ".md", ".txt", ".docx", ".csv", ".xlsx"]

def fetch_file_metadata(file_path: str) -> Dict:
    """
    Extract metadata and a content preview from a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        Dict: A dictionary containing metadata such as name, path, size (MB),
              creation/modification timestamps, extension, and content preview (if supported).
    """
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
            except (IOError) as e:
                print(f"[ERROR] PDF read failed: {file_path} — {e}")

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

    except (FileNotFoundError) as e:
        print(f"[ERROR] Failed to scan {file_path}: {str(e)}")
        return {}

def scan_directory(root_dir: str, extensions: List[str] = None) -> List[Dict]:
    """
    Recursively scans a directory and returns metadata for all supported files.

    Args:
        root_dir (str): Root directory to scan.
        extensions (List[str], optional): List of file extensions to include. Defaults to supported types.

    Returns:
        List[Dict]: List of metadata dictionaries for each file.
    """
    extensions = extensions or SUPPORTED_EXTENSIONS
    files_metadata = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                metadata = fetch_file_metadata(file_path)
                if metadata:
                    files_metadata.append(metadata)

    return files_metadata
