import traceback
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
        frame = np.frombuffer(raw, dtype=np.uint8).reshape(FRAME_SHAPE)
        prediction_request = PredictionRequest(frame_id=frame_id, frame_data=frame)
        logger.info(f"Successfully received frame: {frame_id}")
        result = model_manager.predict(prediction_request)
        prediction_response = PredictionResponse(frame_id=frame_id, predictions=result)
    
    except ValueError as e:
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    return prediction_response
