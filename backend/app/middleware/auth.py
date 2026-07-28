import jwt
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from app.config import JWT_SECRET

EXCLUDED_PATHS = {"/api/auth/login", "/api/health"}


async def auth_middleware(request: Request, call_next):
    try:
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if request.url.path.startswith("/api/"):
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Yetkisiz erişim"})

            token = auth.split(" ", 1)[1]
            try:
                jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Geçersiz token"})

        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Sunucu hatası: {str(e)[:100]}"})
