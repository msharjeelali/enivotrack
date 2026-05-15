from fastapi import APIRouter
from app.services.kafka_producer import kafka_producer
from app.services.stream_manager import stream_manager
from app.services.logger import AppLogger


router = APIRouter(tags=["health"])

logger = AppLogger.get_logger(__name__)


@router.get("/health", status_code=200)
async def health_check() -> dict:
    active_streams = [
        w for w in stream_manager.all()
        if w.status.value == "running"
    ]

    
    logger.info("Health check passed")
    return {
        "status": "ok",
        "kafka_connected": kafka_producer.producer is not None,
        "active_streams": len(active_streams),
        "total_streams": len(stream_manager.all()),
    }