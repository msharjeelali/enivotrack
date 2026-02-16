import os
import requests
from dotenv import load_dotenv

load_dotenv()

AI_SERVICE_URL=os.getenv("AI_SERVICE_URL")

def call_prediction_service(image_bytes):
    try:
        file = {"file": ('frame.jpg', image_bytes, 'image/jpeg')}
        response = requests.post(AI_SERVICE_URL + "/predict", file, timeout=0.5)

        if response.status_code == 200:
            data: List[Dict[str: any]] = response.json()
            return data
    
    except Exception as exp:
        print(f"AI Service Network Error: {exp}")

    return None
