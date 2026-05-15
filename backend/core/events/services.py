import logging
import os
from datetime import datetime
from uuid import UUID

import cv2
import numpy as np
from django.conf import settings

from .models import SmokeEvent

logger = logging.getLogger(__name__)


def save_smoke_event(
    frame: np.ndarray,
    confidence: float,
    intensity: float,
    camera_id: UUID | None = None,
) -> SmokeEvent | None:
    try:
        # build path
        now = datetime.now()
        relative_dir = f"smoke_events/{now.strftime('%Y/%m/%d')}"
        absolute_dir = settings.MEDIA_ROOT / relative_dir
        os.makedirs(absolute_dir, exist_ok=True)

        filename = f"{now.strftime('%H%M%S%f')}.jpg"
        relative_path = f"{relative_dir}/{filename}"
        absolute_path = settings.MEDIA_ROOT / relative_path

        # save image
        cv2.imwrite(str(absolute_path), frame)
        logger.info(f"Smoke frame saved to {absolute_path}")

        # save db record
        event = SmokeEvent.objects.create(
            camera_id=camera_id,
            image=relative_path,
            confidence=confidence,
            intensity=intensity,
        )
        logger.info(f"Smoke event recorded: {event.id}")
        return event

    except Exception as e:
        logger.error(f"Failed to save smoke event: {e}", exc_info=True)
        return None