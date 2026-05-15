import asyncio
import cv2
import logging
from uuid import UUID
from app.models.stream import StreamStatus
from app.services.kafka_producer import kafka_producer
from app.config import KAFKA_TOPIC_PREFIX

logger = logging.getLogger(__name__)

RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 5  # seconds


class StreamWorker:
    def __init__(self, camera_id: UUID, stream_url: str):
        self.camera_id = str(camera_id)
        self.stream_url = stream_url
        self.status = StreamStatus.STOPPED
        self.frames_sent = 0
        self.error = None
        self._task = None

    @property
    def topic(self) -> str:
        return f"{KAFKA_TOPIC_PREFIX}.{self.camera_id}"

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self.status = StreamStatus.STOPPED
        logger.info(f"Stream {self.camera_id} stopped")

    async def _run(self):
        self.status = StreamStatus.RUNNING
        attempts = 0

        while attempts < RECONNECT_ATTEMPTS:
            cap = cv2.VideoCapture(self.stream_url)

            if not cap.isOpened():
                attempts += 1
                logger.warning(
                    f"Could not open stream {self.camera_id}, "
                    f"attempt {attempts}/{RECONNECT_ATTEMPTS}"
                )
                await asyncio.sleep(RECONNECT_DELAY)
                continue

            attempts = 0  # reset on successful connect
            logger.info(f"Stream {self.camera_id} connected")

            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        logger.warning(f"Stream {self.camera_id} lost, reconnecting...")
                        break

                    frame = cv2.resize(frame, (640, 480))
                    _, buffer = cv2.imencode(
                        ".jpg", frame,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    )

                    kafka_producer.send_frame(
                        self.topic,
                        buffer.tobytes(),
                        self.camera_id,
                    )
                    self.frames_sent += 1

                    await asyncio.sleep(0)  # yield to event loop

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Stream {self.camera_id} error: {e}", exc_info=True)
                self.error = str(e)
                attempts += 1
                await asyncio.sleep(RECONNECT_DELAY)
            finally:
                cap.release()

        self.status = StreamStatus.ERROR
        self.error = f"Failed after {RECONNECT_ATTEMPTS} reconnect attempts"
        logger.error(f"Stream {self.camera_id} failed permanently")


class StreamManager:
    def __init__(self):
        self._streams: dict[str, StreamWorker] = {}

    def get(self, camera_id: str) -> StreamWorker | None:
        return self._streams.get(camera_id)

    def all(self) -> list[StreamWorker]:
        return list(self._streams.values())

    async def start(self, camera_id: UUID, stream_url: str) -> StreamWorker:
        key = str(camera_id)
        if key in self._streams:
            raise ValueError(f"Stream {camera_id} already running")
        worker = StreamWorker(camera_id, stream_url)
        self._streams[key] = worker
        await worker.start()
        return worker

    async def stop(self, camera_id: UUID) -> None:
        key = str(camera_id)
        worker = self._streams.pop(key, None)
        if not worker:
            raise ValueError(f"Stream {camera_id} not found")
        await worker.stop()

    async def stop_all(self):
        for worker in list(self._streams.values()):
            await worker.stop()
        self._streams.clear()


stream_manager = StreamManager()