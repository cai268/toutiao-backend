from fastapi import APIRouter

from schemas.common import HealthResponse
from config.chat_conf import get_settings

__version__ = "0.1.0"

router = APIRouter(prefix="/api/health",tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        version=__version__,
    )
