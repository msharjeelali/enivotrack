from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.models.stream import StartStreamRequest, StreamStatus, StreamStatusResponse
from app.services.stream_manager import stream_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["streams"])


@router.post("/streams/start", status_code=201)
async def start_stream(body: StartStreamRequest) -> StreamStatusResponse:
    try:
        worker = await stream_manager.start(body.camera_id, body.stream_url)
        return StreamStatusResponse(
            camera_id=body.camera_id,
            status=worker.status,
            frames_sent=worker.frames_sent,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to start stream: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to start stream")


@router.post("/streams/{camera_id}/stop", status_code=200)
async def stop_stream(camera_id: UUID) -> StreamStatusResponse:
    try:
        worker = stream_manager.get(str(camera_id))
        if not worker:
            raise HTTPException(status_code=404, detail="Stream not found")
        await stream_manager.stop(camera_id)
        return StreamStatusResponse(
            camera_id=camera_id,
            status=StreamStatus.STOPPED,
            frames_sent=worker.frames_sent,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop stream: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to stop stream")


@router.get("/streams", status_code=200)
async def list_streams() -> list[StreamStatusResponse]:
    return [
        StreamStatusResponse(
            camera_id=w.camera_id,
            status=w.status,
            frames_sent=w.frames_sent,
            error=w.error,
        )
        for w in stream_manager.all()
    ]


@router.get("/streams/{camera_id}", status_code=200)
async def get_stream(camera_id: UUID) -> StreamStatusResponse:
    worker = stream_manager.get(str(camera_id))
    if not worker:
        raise HTTPException(status_code=404, detail="Stream not found")
    return StreamStatusResponse(
        camera_id=camera_id,
        status=worker.status,
        frames_sent=worker.frames_sent,
        error=worker.error,
    )