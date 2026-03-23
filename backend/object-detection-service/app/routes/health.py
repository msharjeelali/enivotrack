from fastapi import APIRouter, HTTPException

from app.services.model_manager import model_manager
from app.services.logger import AppLogger

router = APIRouter(tags=["health"])

logger = AppLogger.get_logger(__name__)


@router.get("/health", status_code=200)
async def health_check() -> dict:

    if not model_manager.check_health():
        logger.error("Health check failed: models not loaded")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unavailable",
                "models": {
                    "smoke": model_manager.smoke_model is not None,
                    "vehicle": model_manager.vehicle_model is not None,
                    "plate": model_manager.plate_model is not None,
                    "ocr": model_manager.ocr is not None,
                },
            },
        )

    logger.info("Health check passed")
    return {
        "status": "ok",
        "models": {
            "smoke": model_manager.smoke_model is not None,
            "vehicle": model_manager.vehicle_model is not None,
            "plate": model_manager.plate_model is not None,
            "ocr": model_manager.ocr is not None,
        },
    }
