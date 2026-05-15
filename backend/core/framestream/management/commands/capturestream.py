import os
import logging

import cv2
import numpy as np
from django.core.cache import cache
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from framestream.services import call_prediction_service
from events.services import save_smoke_event


logger = logging.getLogger(__name__)

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "camera.test")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "django-consumer")


def connect_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
    )


def decode_frame(frame_bytes: bytes) -> np.ndarray | None:
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        logger.warning("Failed to decode frame")
    return frame


def draw_predictions(frame: np.ndarray, predictions: list) -> np.ndarray:
    for det in predictions:
        bbox = det.get("bbox", {})
        x1 = int(bbox.get("x1", 0))
        y1 = int(bbox.get("y1", 0))
        x2 = int(bbox.get("x2", 0))
        y2 = int(bbox.get("y2", 0))
        confidence = det.get("confidence", 0)
        track_id = det.get("track_id")

        color = (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        label = f"ID:{track_id} {confidence:.2f}" if track_id else f"{confidence:.2f}"
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_y = max(y1, lh + 6)
        cv2.rectangle(frame, (x1, label_y - lh - 6), (x1 + lw, label_y), color, -1)
        cv2.putText(frame, label, (x1, label_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        plate = det.get("plate")
        if plate:
            pb = plate.get("bbox", {})
            px1 = x1 + int(pb.get("x1", 0))
            py1 = y1 + int(pb.get("y1", 0))
            px2 = x1 + int(pb.get("x2", 0))
            py2 = y1 + int(pb.get("y2", 0))
            plate_text = plate.get("plate_text") or "?"
            cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 255, 255), 2)
            (pw, ph), _ = cv2.getTextSize(plate_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (px1, py2), (px1 + pw, py2 + ph + 6), (0, 255, 255), -1)
            cv2.putText(frame, plate_text, (px1, py2 + ph + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    return frame


class Command(BaseCommand):
    help = "Consume frames from Kafka, run predictions and display results"

    def handle(self, *args, **options):
        try:
            consumer = connect_consumer()
            logger.info(f"Connected to Kafka — topic: {KAFKA_TOPIC}")
            self.stdout.write(self.style.SUCCESS(f"Consumer started on topic: {KAFKA_TOPIC}"))
        except KafkaError as e:
            logger.error(f"Could not connect to Kafka: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Could not connect to Kafka: {e}"))
            return

        self.stdout.write("Press 'q' to quit")

        try:
            for msg in consumer:
                # decode jpeg from kafka
                frame = decode_frame(msg.value)
                if frame is None:
                    continue

                # resize to 640x640 and convert to raw bytes for prediction service
                frame_resized = cv2.resize(frame, (640, 640))
                raw_bytes = frame_resized.tobytes()  # ← send this to prediction service

                predictions = call_prediction_service(raw_bytes)

                if predictions:
                    frame_resized = draw_predictions(frame_resized, predictions)
                    cache.set("latest_predictions", predictions, timeout=60)

                    for det in predictions:
                        save_smoke_event(
                            frame=frame_resized,
                            confidence=det.get("confidence", 0.0),
                            intensity=det.get("intensity", 0.0),
                        )

                _, buffer = cv2.imencode(".jpg", frame_resized)
                cache.set("latest_frame", buffer.tobytes(), timeout=60)

                cv2.imshow("Live Stream", frame_resized)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        except KafkaError as e:
            logger.error(f"Kafka error: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Kafka error: {e}"))

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))

        finally:
            consumer.close()
            cv2.destroyAllWindows()
            self.stdout.write(self.style.SUCCESS("Consumer stopped. Resources released."))