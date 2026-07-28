import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, analyze, report, auth
from app.middleware.auth import auth_middleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("lensecode")

app = FastAPI(title="lensecode", version="1.0.0")

allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://lensecode.com")
if allowed_origins == "*":
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in allowed_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    logger.warning("LLM API anahtarları bulunamadı. AI analizi fallback modunda çalışacak.")

app.middleware("http")(auth_middleware)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(report.router, prefix="/api", tags=["report"])

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "lensecode"}

logger.info("lensecode backend başlatıldı")