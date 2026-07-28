import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.routes import analyze, auth, report, upload
from app.middleware.auth import auth_middleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("lensecode")

app = FastAPI(title="lensecode", version="1.0.0")

allowed_origins = os.getenv("CORS_ORIGINS", "").strip()
railway_origin = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
if railway_origin:
    railway_origin = f"https://{railway_origin}"

origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
if railway_origin and railway_origin not in origins:
    origins.append(railway_origin)

if not origins or allowed_origins == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS izinli origin'ler: {origins}")

if not config.ANTHROPIC_API_KEY and not config.OPENAI_API_KEY:
    logger.warning("LLM API anahtarları bulunamadı. AI analizi fallback modunda çalışacak.")

try:
    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Yükleme dizini: {config.UPLOAD_DIR}")
except OSError as e:
    logger.error(f"Yükleme dizini oluşturulamadı: {config.UPLOAD_DIR} ({e})")
    raise

app.middleware("http")(auth_middleware)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(report.router, prefix="/api", tags=["report"])


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "lensecode",
        "llm_configured": bool(config.ANTHROPIC_API_KEY or config.OPENAI_API_KEY),
        "semgrep_enabled": config.ENABLE_SEMGREP,
    }


logger.info("lensecode backend başlatıldı")
