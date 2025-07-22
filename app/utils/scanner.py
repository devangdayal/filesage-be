import os
from pathlib import Path

SUPPORTED_EXTENSIONS = [".pdf",".md",".txt",".docx",".csv","xlsx"]

def scan_directory(directory:str):
    directory = Path(directory).resolve()
    
    found_files = []
   
    for root, _,files in os.walk(directory):
        for file in files:
            extension = Path(file).suffix.lower()
            if extension in SUPPORTED_EXTENSIONS:
                full_path = Path(root)/file
                found_files.append({
                    "path":(full_path),
                    "name": file,
                    "extension":extension
                })
             
    return found_files