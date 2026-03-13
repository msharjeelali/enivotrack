from fastapi import APIRouter, HTTPException

from app.services.model_manager import model_manager

router = APIRouter(tags=["health"])


@router.get("/health", status_code=200)
async def health_check():
    
    if not model_manager.model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"status": "ok"}
