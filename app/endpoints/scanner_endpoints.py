from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.scanner import scan_directory

router = APIRouter()

class ScannerRequest(BaseModel):
    path: str

@router.get("/health-check")
def read_root():
    return {"message": "FileSage backend is up 🚀"}

@router.post("/find-files")
def scan_files(request: ScannerRequest):
    result = scan_directory(request.path)
    return result
