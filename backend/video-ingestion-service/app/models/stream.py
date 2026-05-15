from pydantic import BaseModel
from uuid import UUID
from enum import Enum


class StreamStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class StartStreamRequest(BaseModel):
    camera_id: UUID
    stream_url: str


class StreamStatusResponse(BaseModel):
    camera_id: UUID
    status: StreamStatus
    frames_sent: int
    error: str | None = None