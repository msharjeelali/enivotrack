import logging
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File

app = FastAPI()
model = YOLO("yolov8l.pt") 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.post("/predict")
async def model_predict(frame: UploadFile = File(...)):
    contents = await frame.read()
    image = Image.open(BytesIO(contents))
    
    results = model(image)
    
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls),
                "name": r.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": box.xyxy.tolist()
            })
    logger.debug(f"Detections: {detections}")
            
    return {"detections": detections}