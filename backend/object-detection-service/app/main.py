from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.routes.health import router as health_router
from app.routes.v1.prediction import router as prediction_router
from app.services.model_manager import model_manager
from app.config import LOG_LEVEL, LOG_FILE
from app.services.logger import AppLogger
from app.middleware.auth import APIKeyMiddleware


AppLogger.setup(log_level=LOG_LEVEL, log_file=LOG_FILE)
logger = AppLogger.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        model_manager.load_model()
        logger.info("Application startup complete.")
        yield
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    finally:
        logger.info("Application shutdown.")


app = FastAPI(
    lifespan=lifespan, title="Envirotrack - Object Detection Service", version="1.0.0"
)

app.add_middleware(APIKeyMiddleware)

app.include_router(health_router)
app.include_router(prediction_router, prefix="/api/v1")
