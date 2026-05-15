import logging
import uuid
from uuid import UUID

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


def call_prediction_service(frame_bytes: bytes, frame_id: UUID | None = None) -> list | None:
    if not settings.AI_SERVICE_URL:
        logger.error("AI_SERVICE_URL is not set")
        return None

    if frame_id is None:
        frame_id = uuid.uuid4()

    try:
        response = httpx.post(
            f"{settings.AI_SERVICE_URL}/api/v1/predict",
            headers={
                "frame-id": str(frame_id),
                "Content-Type": "application/octet-stream",
                "X-API-Key": settings.AI_SERVICE_API_KEY,
            },
            content=frame_bytes,
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("predictions", [])

    except httpx.TimeoutException:
        logger.error("Prediction service timed out")
    except httpx.HTTPStatusError as e:
        logger.error(
            f"Prediction service error: {e.response.status_code} - {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling prediction service: {e}", exc_info=True)

    return None