from kafka import KafkaProducer
from kafka.errors import KafkaError
from app.config import KAFKA_HOST, KAFKA_PORT
import logging

logger = logging.getLogger(__name__)


class KafkaFrameProducer:
    def __init__(self):
        self.producer = None

    def connect(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
                api_version=(3, 7, 0),
                linger_ms=10,
                compression_type="gzip",   # compress frames
                max_request_size=10485760,  # 10MB max frame size
            )
            logger.info("Kafka producer connected")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}", exc_info=True)
            raise RuntimeError(f"Kafka connection failed: {e}")

    def send_frame(self, topic: str, frame_bytes: bytes, camera_id: str):
        if not self.producer:
            raise RuntimeError("Kafka producer not connected")
        try:
            self.producer.send(
                topic,
                value=frame_bytes,
                key=camera_id.encode("utf-8"),  # key by camera_id for partitioning
            )
        except KafkaError as e:
            logger.error(f"Failed to send frame: {e}", exc_info=True)
            raise

    def close(self):
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


kafka_producer = KafkaFrameProducer()