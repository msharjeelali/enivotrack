import numpy as np
import easyocr

from ultralytics import YOLO
from roboflow import Roboflow

from app.services.logger import AppLogger
from app.config import (
    VEHICLE_MODEL_PATH,
    SMOKE_MODEL_PATH,
    ROBOFLOW_API_KEY,
    PROJECT_VERSION,
    PLATE_DETECTION_PROJECT,
    SMOKE_DETECTION_ENABLED,
)
from app.models.prediction import (
    yolo_to_prediction_response,
    PredictionRequest,
    Detection,
    PlateDetection,
    BoundingBox,
)

logger = AppLogger.get_logger(__name__)


class ModelManager:
    def __init__(self):
        self.smoke_model = None
        self.vehicle_model = None
        self.plate_model = None
        self.ocr = None

    def check_health(self) -> bool:
        return all([self.smoke_model, self.vehicle_model, self.plate_model, self.ocr])

    def load_model(self) -> None:
        logger.info(f"Loading smoke model from {SMOKE_MODEL_PATH}")
        logger.info(f"Loading vehicle model from {VEHICLE_MODEL_PATH}")
        logger.info(f"Loading plate model from Roboflow {PLATE_DETECTION_PROJECT}")

        try:
            self.smoke_model = YOLO(SMOKE_MODEL_PATH)
            logger.info("Smoke model loaded successfully")

            self.vehicle_model = YOLO(VEHICLE_MODEL_PATH)
            logger.info("Vehicle model loaded successfully")

            rf = Roboflow(api_key=ROBOFLOW_API_KEY)
            project = rf.workspace().project(PLATE_DETECTION_PROJECT)
            self.plate_model = project.version(PROJECT_VERSION).model
            logger.info("Plate detection model loaded successfully")

            self.ocr = easyocr.Reader(["en"], gpu=False)
            logger.info("OCR loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load model: {e}", exc_info=True)
            raise RuntimeError(f"Model loading failed: {e}")

    def _detect_plate(self, vehicle_crop: np.ndarray) -> PlateDetection | None:
        if vehicle_crop.size == 0:
            return None

        try:
            plate_results = self.plate_model.predict(vehicle_crop, confidence=50)
            predictions = plate_results.json().get("predictions", [])

            if not predictions:
                return None

            best = max(predictions, key=lambda p: p["confidence"])

            x1 = max(0, int(best["x"] - best["width"] / 2))
            y1 = max(0, int(best["y"] - best["height"] / 2))
            x2 = min(vehicle_crop.shape[1], int(best["x"] + best["width"] / 2))
            y2 = min(vehicle_crop.shape[0], int(best["y"] + best["height"] / 2))

            plate_crop = vehicle_crop[y1:y2, x1:x2]

            if plate_crop.size == 0:
                return None

            ocr_results = self.ocr.readtext(plate_crop)
            plate_text = " ".join([text for _, text, _ in ocr_results]).strip() or None

            return PlateDetection(
                bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                plate_text=plate_text,
                confidence=float(best["confidence"]) / 100,
            )

        except Exception as e:
            logger.error(f"Plate detection failed: {e}", exc_info=True)
            return None

    def predict(self, request: PredictionRequest) -> list[Detection]:
        if not self.check_health():
            raise RuntimeError("Models not loaded")

        frame = request.frame_data

        if SMOKE_DETECTION_ENABLED:
            smoke_results = self.smoke_model.track(
                frame, tracker="bytetrack.yaml", persist=True
            )
            smoke_detections = yolo_to_prediction_response(frame, smoke_results[0])
            logger.info(f"Smoke detections for {request.frame_id}: {smoke_detections}")

        vehicle_results = self.vehicle_model.track(
            frame, tracker="bytetrack.yaml", persist=True
        )
        detections = yolo_to_prediction_response(frame, vehicle_results[0])

        for detection, box in zip(detections, vehicle_results[0].boxes):
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            vehicle_crop = frame[y1:y2, x1:x2]
            detection.plate = self._detect_plate(vehicle_crop)

        logger.info(f"Vehicle detections for {request.frame_id}: {detections}")
        return detections


model_manager = ModelManager()
