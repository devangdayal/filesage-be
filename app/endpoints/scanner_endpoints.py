""" Scanning the files"""
import os
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.model.request import PathRequest
from app.utils.scanner import scan_directory

MAX_WORKERS = min(32, os.cpu_count() * 5)

router = APIRouter()

@router.get("/health-check")
def read_root():
    """Health Check Endpoint"""
    return {"message": "FileSage backend is up 🚀"}

@router.post("/scan-directory")
def scan_files(request: PathRequest):
    """Scan the Directory for Supported files i.e. [".pdf", ".md", ".txt", ".docx", ".csv", ".xlsx"]"""
    try:
        logging.info("Scanning directory: %s with MAX_WORKERS= %s ",{request.path},{MAX_WORKERS})
        
        result = scan_directory(root_dir=request.path, max_workers=MAX_WORKERS)
        return {
            "status": "success",
            "total_files": len(result),
            "data": result
        }
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "Directory not found"})
    
    
    except Exception as e:
        logging.exception("Unexpected error during file scan")
        return JSONResponse(status_code=500, content={"error": str(e)})
