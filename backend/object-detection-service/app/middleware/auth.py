from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import API_KEY

EXCLUDED_PATHS = {
    "/docs",
    "/openapi.json",
    "/redoc",
}

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "API key missing"}
            )

        if api_key != API_KEY:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API key"}
            )

        return await call_next(request)