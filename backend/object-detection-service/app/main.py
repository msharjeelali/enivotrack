from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.prediction import router as prediction_router
from contextlib import asynccontextmanager
from app.services.model_manager import model_manager
from app.config import MODEL_PATH, LOG_LEVEL, LOG_FILE
from app.services.logger import AppLogger


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_manager.load_model(MODEL_PATH)
    AppLogger.setup(log_level=LOG_LEVEL, log_file=LOG_FILE)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(prediction_router)
