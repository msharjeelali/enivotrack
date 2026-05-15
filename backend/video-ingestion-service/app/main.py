from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.v1.streams import router as streams_router
from app.routers.health import router as health_router
from app.services.kafka_producer import kafka_producer
from app.services.stream_manager import stream_manager
import logging

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_producer.connect()
    logger.info("Video ingestion service started")
    yield
    await stream_manager.stop_all()
    kafka_producer.close()
    logger.info("Video ingestion service stopped")


app = FastAPI(
    title="Envirotrack - Video Ingestion Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(streams_router, prefix="/api/v1")