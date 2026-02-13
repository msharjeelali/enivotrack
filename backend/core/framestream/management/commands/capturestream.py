import os
import cv2 
import numpy as np 
from dotenv import load_dotenv
from kafka import KafkaConsumer
from django.core.management.base import BaseCommand, CommandError

load_dotenv()

KAFKA_IP = os.getenv('KAFKA_HOST_IP')
KAFKA_PORT = os.getenv('KAFKA_PORT')
TOPIC = os.getenv('KAFKA_TOPIC')

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
                frame_array = np.frombuffer(msg.value, dtype=np.uint8)             
                img = cv2.imdecode(frame_array, cv2.IMREAD_COLOR) 
                
                if img is not None: 
                    cv2.imshow("Live Kafka Stream", img) 
                
                # Use a tiny waitKey to keep the UI responsive
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break 
        
        except Exception as e:
            print(f"Loop error: {e}")
        finally: 
            consumer.close() 
            cv2.destroyAllWindows()