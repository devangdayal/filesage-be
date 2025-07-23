from fastapi import APIRouter
from app.endpoints import content_extractor_endpoint, scanner_endpoints


router = APIRouter()
router.include_router(scanner_endpoints.router, prefix="/v1", tags=["filesage"])
router.include_router(
    content_extractor_endpoint.router, prefix="/v1", tags=["filesage"]
)
