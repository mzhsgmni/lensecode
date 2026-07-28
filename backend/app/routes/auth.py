import os
import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

PASSWORD = os.getenv("LENSCODE_PASSWORD", "4omaz")
JWT_SECRET = os.getenv("JWT_SECRET", "lensecode_gizli_anahtar_2024")

class LoginRequest(BaseModel):
    password: str

@router.post("/auth/login")
def login(req: LoginRequest):
    if req.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    payload = {"authenticated": True, "exp": datetime.utcnow() + timedelta(days=7)}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"token": token}