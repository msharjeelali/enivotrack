import numpy as np
from uuid import UUID
from fastapi import APIRouter, HTTPException, Request, Header

from app.services.logger import AppLogger
from app.services.model_manager import model_manager
from app.models.prediction import PredictionRequest, PredictionResponse

router = APIRouter(tags=["prediction"])

FRAME_SHAPE = (640, 640, 3)
EXPECTED_BYTES = 640 * 640 * 3

logger = AppLogger.get_logger(__name__)


@router.post("/predict", status_code=200)
async def predict(
    request: Request,
    frame_id: UUID = Header(..., alias="frame-id"),
) -> PredictionResponse:

    raw = await request.body()

    if not raw:
        raise HTTPException(status_code=400, detail="Request body is empty")

    if len(raw) != EXPECTED_BYTES:
        raise HTTPException(
            status_code=400, detail=f"Expected {EXPECTED_BYTES} bytes, got {len(raw)}"
        )

    try:
        frame = (
            np.frombuffer(raw, dtype=np.uint8).reshape(FRAME_SHAPE).copy()
        )  # ✅ writable
        prediction_request = PredictionRequest(frame_id=frame_id, frame_data=frame)
        logger.info(f"Successfully received frame: {frame_id}")
        result = model_manager.predict(prediction_request)
        return PredictionResponse(frame_id=frame_id, predictions=result)

    except ValueError as e:
        logger.error(f"Validation error for frame {frame_id}: {e}", exc_info=True)
        raise HTTPException(status_code=422, detail="Invalid frame data")

    except RuntimeError as e:
        logger.error(f"Model error for frame {frame_id}: {e}", exc_info=True)
        raise HTTPException(status_code=503, detail="Model unavailable")

    except Exception as e:
        logger.error(f"Unexpected error for frame {frame_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
