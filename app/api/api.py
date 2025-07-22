from fastapi import APIRouter
from app.endpoints import endpoints


router = APIRouter()
router.include_router(endpoints.router, prefix="/v1", tags=["v1"])