import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
if not ROBOFLOW_API_KEY:
    raise ValueError("ROBOFLOW_API_KEY is not set in environment")

PLATE_DETECTION_PROJECT = os.getenv(
    "PLATE_DETECTION_PROJECT", "license-plate-recognition-rxg4e"
)
PROJECT_VERSION = int(os.getenv("PROJECT_VERSION", 11))

SMOKE_MODEL_PATH = MODELS_DIR / "smoke_model.pt"
VEHICLE_MODEL_PATH = MODELS_DIR / "yolov8m.pt"

SMOKE_DETECTION_ENABLED = os.getenv("SMOKE_DETECTION_ENABLED", "false").lower()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set in environment")
