from ultralytics import YOLO
from fastapi import RunTimeError

from app.services.logger import AppLogger
from app.models.prediction import (
    yolo_to_prediction_response,
    PredictionRequest,
    Detection,
)

logger = AppLogger.get_logger(__name__)


class ModelManager:
    def __init__(self):
        
        self.model = None

    def load_model(self, model_path: str) -> None:
        
        logger.info(f"Loading model from {model_path}")
        
        try:
            self.model = YOLO(model_path)
            logger.info("Model loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load model: {e}")

    def predict(self, request: PredictionRequest) -> list[Detection]:
        
        if not self.model:
            raise RunTimeError("Model not loaded")
        
        results = self.model.predict(request.frame_data)
        results = yolo_to_prediction_response(request.frame_data, results[0])
        logger.info(f"Results for {request.frame_id}: {results}")
        return results


model_manager = ModelManager()
