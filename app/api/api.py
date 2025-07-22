from fastapi import APIRouter
from app.endpoints import scanner_endpoints


router = APIRouter()
router.include_router(scanner_endpoints.router, prefix="/v1", tags=["filesage"])