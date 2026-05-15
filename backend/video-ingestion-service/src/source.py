import cv2
import sys
import os
import logging
import argparse
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "camera.test")

if not KAFKA_HOST:
    raise ValueError("KAFKA_HOST is not set")


def connect_kafka() -> KafkaProducer:
    try:
        producer = KafkaProducer(
            bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
            security_protocol="PLAINTEXT",
            api_version=(3, 7, 0),
            linger_ms=10,
            compression_type="gzip",
            max_request_size=10485760,
        )
        logger.info("Kafka producer connected")
        return producer
    except KafkaError as e:
        logger.error(f"Could not connect to Kafka: {e}")
        sys.exit(1)


def get_capture_source(source: str) -> cv2.VideoCapture:
    if source == "camera":
        cap = cv2.VideoCapture(0)
        logger.info("Using laptop camera")
    else:
        if not os.path.exists(source):
            logger.error(f"Video file not found: {source}")
            sys.exit(1)
        cap = cv2.VideoCapture(source)
        logger.info(f"Using video file: {source}")

    if not cap.isOpened():
        logger.error(f"Could not open source: {source}")
        sys.exit(1)

    return cap


def stream(source: str, topic: str) -> None:
    producer = connect_kafka()
    cap = get_capture_source(source)

    logger.info(f"Streaming to topic: {topic}")
    logger.info("Press Ctrl+C to quit")

    frames_sent = 0

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                if source != "camera":
                    logger.info("Video file ended")
                else:
                    logger.warning("Failed to read frame from camera")
                break

            frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode(
                ".jpg", frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            )

            if ret:
                producer.send(topic, buffer.tobytes())
                frames_sent += 1
                logger.info(f"Sent frame {frames_sent} — size: {len(buffer)} bytes")

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt — stopping stream")

    except Exception as e:
        logger.error(f"Streaming error: {e}", exc_info=True)

    finally:
        cap.release()
        producer.flush()
        producer.close()
        logger.info(f"Done. Total frames sent: {frames_sent}")


def parse_args():
    parser = argparse.ArgumentParser(description="Kafka Frame Producer")
    parser.add_argument(
        "--source",
        type=str,
        default="camera",
        help="'camera' for laptop camera or path to video file e.g. --source video.mp4",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=KAFKA_TOPIC,
        help=f"Kafka topic to publish to (default: {KAFKA_TOPIC})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    stream(source=args.source, topic=args.topic)