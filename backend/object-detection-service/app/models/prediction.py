import cv2
import numpy as np
from uuid import UUID
from typing import Annotated, Any
from pydantic_core import core_schema
from pydantic import BaseModel, field_validator, Field, ConfigDict


class NumpyArray:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: Any) -> np.ndarray:
        
        if isinstance(value, np.ndarray):
            return value
        
        if isinstance(value, list):
        
            try:
                return np.array(value, dtype=np.uint8)
        
            except (ValueError, TypeError) as e:
                raise ValueError(f"List could not be converted to uint8 array: {e}")
        
        raise ValueError(f"Expected np.ndarray or list, got {type(value).__name__}")


class PredictionRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    frame_id: UUID
    frame_data: Annotated[np.ndarray, NumpyArray]

    @field_validator("frame_data", mode="after")
    @classmethod
    def validate_frame_data(cls, value: np.ndarray) -> np.ndarray:
        
        if value.ndim not in (2, 3):
            raise ValueError("frame_data must be a 2D or 3D array")

        if value.ndim == 3 and value.shape[2] not in (3, 4):
            raise ValueError("3D frame_data must have 3 or 4 channels")

        if value.dtype != np.uint8:
            raise ValueError("frame_data must be uint8")

        h, w = value.shape[:2]
        if h != 640 or w != 640:
            raise ValueError(f"Expected 640x640 frame, got {h}x{w}")

        return value


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    bbox: BoundingBox
    confidence: float = Field(..., ge=0.0, le=1.0)
    smoke: bool
    intensity: float = Field(..., ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    frame_id: UUID
    predictions: list[Detection]


def calculate_intensity(frame: np.ndarray, box) -> float:
    
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    smoke_region = frame[int(y1) : int(y2), int(x1) : int(x2)]
    
    if smoke_region.size == 0:
        return 0.0
    
    gray = cv2.cvtColor(smoke_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(smoke_region, cv2.COLOR_BGR2GRAY)
    intensity = gray.mean() / 255
    return intensity


def yolo_to_prediction_response(frame: np.ndarray, result) -> list[Detection]:
    
    detections = []

    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = result.names[class_id]
        smoke = class_name.lower() == "smoke"
        intensity = calculate_intensity(frame, box)

        detections.append(
            Detection(
                bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                confidence=confidence,
                smoke=smoke,
                intensity=intensity,
            )
        )

    return detections
