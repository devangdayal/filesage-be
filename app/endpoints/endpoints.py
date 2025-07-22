from fastapi import APIRouter


router = APIRouter()


@router.get("/health-check")
def read_root():
    return {"message": "FileSage backend is up 🚀"}