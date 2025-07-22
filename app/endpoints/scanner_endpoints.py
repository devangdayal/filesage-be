from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.scanner import scan_directory
from app.model.scanner import ScannerRequest

router = APIRouter()

@router.get("/health-check")
def read_root():
    """Health Check Endpoint"""
    import sys
    print(sys.executable)
    return {"message": "FileSage backend is up 🚀"}
    


@router.post("/find-files")
def scan_files(request: ScannerRequest):
    """Scan the Directory for Supported files i.e. [".pdf", ".md", ".txt", ".docx", ".csv", ".xlsx"] """
    result = scan_directory(request.path)
    return result
