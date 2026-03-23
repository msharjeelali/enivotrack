from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import API_KEY


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            raise HTTPException(status_code=401, detail="API key missing")

        if api_key != API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API key")

        return await call_next(request)
