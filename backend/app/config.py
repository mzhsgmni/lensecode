import os
import secrets
import warnings
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

for _candidate in (BASE_DIR / ".env", BASE_DIR / "backend" / ".env"):
    if _candidate.is_file():
        load_dotenv(_candidate, override=False)

DEFAULT_PASSWORD = "4omaz"
_MIN_SECRET_BYTES = 32

LENSCODE_PASSWORD = os.getenv("LENSCODE_PASSWORD", "")
if not LENSCODE_PASSWORD:
    LENSCODE_PASSWORD = DEFAULT_PASSWORD
    warnings.warn(
        "LENSCODE_PASSWORD tanimli degil; gecici olarak varsayilan kullaniliyor. "
        "Canliya almadan once .env icinde LENSCODE_PASSWORD ayarla.",
        RuntimeWarning,
        stacklevel=2,
    )

JWT_SECRET = os.getenv("JWT_SECRET", "")
if len(JWT_SECRET.encode("utf-8")) < _MIN_SECRET_BYTES:
    if JWT_SECRET:
        warnings.warn(
            f"JWT_SECRET {_MIN_SECRET_BYTES} bayttan kisa; gecici rastgele bir anahtar uretildi. "
            "Token'lar yeniden baslatmada gecersizlesir. .env icinde en az 32 baytlik bir deger ayarla.",
            RuntimeWarning,
            stacklevel=2,
        )
    JWT_SECRET = secrets.token_urlsafe(48)

TOKEN_EXPIRY_DAYS = int(os.getenv("TOKEN_EXPIRY_DAYS", "7"))

# Giris formu koruması. Tek paylaşılan şifre olduğu için brute force'a
# karşı başarısız denemeler sayılır ve eşik aşılınca IP kilitlenir.
LOGIN_MAX_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS", "5"))
LOGIN_WINDOW_SECONDS = int(os.getenv("LOGIN_WINDOW_SECONDS", "900"))
MAX_TRACKED_CLIENTS = int(os.getenv("MAX_TRACKED_CLIENTS", "10000"))

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

ENABLE_SEMGREP = os.getenv("ENABLE_SEMGREP", "1") not in ("0", "false", "False")
SEMGREP_CONFIG = os.getenv("SEMGREP_CONFIG", "auto")

# Yüklenen projelerin tutulduğu dizin. Railway'de bir volume'a baglamak icin
# UPLOAD_DIR=/data/uploads ayarla.
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR") or (Path(__file__).resolve().parent / "uploads")).resolve()
