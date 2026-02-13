import cv2
import sys
import time
from kafka import KafkaProducer

TOPIC = "test-topic"

def publish_camera():

    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            api_version=(3, 7, 0),
            linger_ms=10
            )
    except Exception as exp:
        print(f"Could not connect to kafka: {exp}")
        return

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera...")
        return
    

    print("Streaming started. Press 'q' to quit.")

    try:
        while(True):
            success, frame = camera.read()
            if not success:
                break

            small_frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            
            if ret:
                producer.send(TOPIC, buffer.tobytes())
                print("Sent frame of size:", len(buffer))

            cv2.imshow('Producer View', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print('Keyboard Interupt Stopping Stream...')
    
    except Exception as exp:
        print(f'Error: {exp}')
    
    finally:
        camera.release()
        cv2.destroyAllWindows()
        producer.flush()
        producer.close()
        
        print('Resource Released')

if __name__ == "__main__":
    publish_camera()
