import os
import cv2 
import numpy as np 
from dotenv import load_dotenv
from kafka import KafkaConsumer
from django.core.management.base import BaseCommand, CommandError
from framestream.services import call_prediction_service

load_dotenv()

KAFKA_IP = os.getenv('KAFKA_HOST_IP', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_HOST_PORT', '9092')
TOPIC = os.getenv('KAFKA_TOPIC', 'camera.frames')

class Command(BaseCommand):
    help = "Start the server to capture frames from kafka"

    def handle(self, *args, **options):
        try: 
            consumer = KafkaConsumer( 
                TOPIC, 
                bootstrap_servers=[f"{KAFKA_IP}:{KAFKA_PORT}"], 
                auto_offset_reset='latest',  # Start from the NEWEST frame
                enable_auto_commit=True, 
                group_id='video-consumer'
                # Removed timeout so it stays active
            )
        except Exception as exp: 
            self.stdout.write(self.style.ERROR(f"Could not connect: {exp}"))
            return 
        
        print("Consumer started. Viewing live stream...") 
        
        try: 
            for msg in consumer: 
                frame_bytes = msg.value             
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                predictions = call_prediction_service(frame_bytes)
                
                if predictions:
                    for det in predictions:
                        bbox = det['bbox']
                        name = det['name']
                        conf = det['confidence']
            
                        start_point = (int(bbox[0]), int(bbox[1]))
                        end_point = (int(bbox[2]), int(bbox[3]))
                        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                        
                        label = f"{name} {conf:.2f}"
                        cv2.putText(frame, label, (int(bbox[0]), int(bbox[1] - 10)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                _, buffer = cv2.imencode('.jpg', frame)
                processed_frame_bytes = buffer.tobytes()
                cache.set('latest_frame', processed_frame_bytes)
                if predictions:
                    cache.set('latest_predictions', predictions)

                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break 
        
        except Exception as e:
            print(f"Loop error: {e}")
        finally: 
            consumer.close() 
            cv2.destroyAllWindows()