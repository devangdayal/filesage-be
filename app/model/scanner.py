from pydantic import BaseModel
class ScannerRequest(BaseModel):
    """Request for Dir Scanning"""
    path: str
