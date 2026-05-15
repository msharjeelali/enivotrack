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
)
from app.models.prediction import (
    SmokeDetection,
    VehicleDetection,
    PlateDetection,
    BoundingBox,
    PredictionRequest,
    yolo_to_smoke_detections,
    yolo_to_vehicle_detections,
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

    def _link_vehicle_to_smoke(  # ✅ inside class
        self,
        smoke_detections: list[SmokeDetection],
        vehicle_detections: list[VehicleDetection],
    ) -> None:
        for vehicle in vehicle_detections:
            vx1, vy1, vx2, vy2 = (
                vehicle.bbox.x1, vehicle.bbox.y1,
                vehicle.bbox.x2, vehicle.bbox.y2,
            )
            best_smoke = None
            best_overlap = 0

            for smoke in smoke_detections:
                sx1, sy1, sx2, sy2 = (
                    smoke.bbox.x1, smoke.bbox.y1,
                    smoke.bbox.x2, smoke.bbox.y2,
                )
                ix1 = max(vx1, sx1)
                iy1 = max(vy1, sy1)
                ix2 = min(vx2, sx2)
                iy2 = min(vy2, sy2)

                if ix2 > ix1 and iy2 > iy1:
                    overlap = (ix2 - ix1) * (iy2 - iy1)
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_smoke = smoke

            if best_smoke:
                best_smoke.vehicle = vehicle

    def predict(self, request: PredictionRequest) -> list[SmokeDetection]:  # ✅ inside class
        if not self.check_health():
            raise RuntimeError("Models not loaded")

        frame = request.frame_data

        smoke_results = self.smoke_model.track(
            frame, tracker="bytetrack.yaml", persist=True
        )
        smoke_detections = yolo_to_smoke_detections(frame, smoke_results[0])

        if not smoke_detections:
            logger.info(f"No smoke detected for frame {request.frame_id}")
            return []

        logger.info(f"{len(smoke_detections)} smoke detection(s) for {request.frame_id}")

        vehicle_results = self.vehicle_model.track(
            frame, tracker="bytetrack.yaml", persist=True
        )
        vehicle_detections = yolo_to_vehicle_detections(vehicle_results[0])

        for vehicle in vehicle_detections:
            x1, y1, x2, y2 = (
                int(vehicle.bbox.x1), int(vehicle.bbox.y1),
                int(vehicle.bbox.x2), int(vehicle.bbox.y2),
            )
            vehicle_crop = frame[y1:y2, x1:x2]
            vehicle.plate = self._detect_plate(vehicle_crop)

        self._link_vehicle_to_smoke(smoke_detections, vehicle_detections)

        logger.info(f"Vehicle detections for {request.frame_id}: {vehicle_detections}")
        return smoke_detections


model_manager = ModelManager()