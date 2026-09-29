import hmac
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.config import JWT_SECRET, LENSCODE_PASSWORD, TOKEN_EXPIRY_DAYS
from app.middleware.rate_limit import client_key, enforce_login_limit, login_limiter

router = APIRouter()


class LoginRequest(BaseModel):
    password: str


@router.post("/auth/login")
def login(req: LoginRequest, request: Request):
    enforce_login_limit(request)
    key = client_key(request)

    if not hmac.compare_digest(req.password.encode(), LENSCODE_PASSWORD.encode()):
        login_limiter.record_failure(key)
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    login_limiter.reset(key)

    payload = {
        "authenticated": True,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"token": token}
