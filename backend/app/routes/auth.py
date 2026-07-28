import hmac
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import JWT_SECRET, LENSCODE_PASSWORD, TOKEN_EXPIRY_DAYS

router = APIRouter()


class LoginRequest(BaseModel):
    password: str


@router.post("/auth/login")
def login(req: LoginRequest):
    if not hmac.compare_digest(req.password.encode(), LENSCODE_PASSWORD.encode()):
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    payload = {
        "authenticated": True,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"token": token}
