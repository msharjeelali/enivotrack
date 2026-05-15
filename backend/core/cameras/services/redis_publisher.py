import json
import logging

import redis
from django.conf import settings

logger = logging.getLogger(__name__)


def publish_camera_event(camera, action: str) -> None:
    """
    Publish camera events to Redis.

    Safety: never crash the API if Redis is unavailable.
    """
    host = getattr(settings, "REDIS_HOST", "localhost")
    port = int(getattr(settings, "REDIS_PORT", 6379))

    payload = {
        "id": camera.id,
        "name": camera.name,
        "rtsp_url": camera.rtsp_url,
        "action": action,
    }

    try:
        client = redis.Redis(host=host, port=port, decode_responses=True)
        client.publish("camera.events", json.dumps(payload))
    except Exception as exc:
        logger.error("Redis publish failed for camera event.", exc_info=exc)

