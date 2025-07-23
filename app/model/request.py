from pydantic import BaseModel


class PathRequest(BaseModel):
    """Request for Dir Scanning"""
    path: str
