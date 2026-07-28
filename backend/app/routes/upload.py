import os
import re
import uuid
import zipfile
import shutil
import subprocess
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("lensecode")
router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_ZIP_MB = 100
MAX_EXTRACT_MB = 500
MAX_FILES = 1000
PROJECT_ID_PATTERN = re.compile(r"^[a-f0-9]{8}$")
FILENAME_PATTERN = re.compile(r"^[\w.\- ]+$")
GITHUB_PATTERN = re.compile(r"^https://github\.com/[a-zA-Z0-9_.\-]+/[a-zA-Z0-9_.\-]+(/.*)?$")

def validate_project_id(pid: str):
    if not PROJECT_ID_PATTERN.match(pid):
        raise HTTPException(status_code=400, detail="Geçersiz proje ID")

def sanitize_filename(name: str) -> str:
    name = os.path.basename(name)
    if not FILENAME_PATTERN.match(name):
        raise HTTPException(status_code=400, detail="Geçersiz dosya adı")
    return name

def safe_path(base: str, *parts: str) -> str:
    joined = os.path.join(base, *parts)
    joined = os.path.realpath(joined)
    base = os.path.realpath(base)
    if not joined.startswith(base):
        raise HTTPException(status_code=400, detail="Geçersiz yol")
    return joined

class URLUpload(BaseModel):
    url: str

@router.post("/upload/zip")
async def upload_zip(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_ZIP_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Dosya çok büyük (max {MAX_ZIP_MB}MB)")

    project_id = str(uuid.uuid4())[:8]
    extract_path = safe_path(UPLOAD_DIR, project_id)
    os.makedirs(extract_path, exist_ok=True)

    temp_zip = os.path.join(UPLOAD_DIR, f"{project_id}.zip")
    try:
        with open(temp_zip, "wb") as f:
            f.write(contents)

        total_size = 0
        file_count = 0
        with zipfile.ZipFile(temp_zip, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                file_count += 1
                total_size += info.file_size
                if file_count > MAX_FILES:
                    raise HTTPException(status_code=400, detail="Çok fazla dosya var (max 1000)")
                if total_size > MAX_EXTRACT_MB * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="Çıkarma boyutu çok büyük (max 500MB)")

            zf.extractall(extract_path)

        logger.info(f"ZIP yüklendi: project_id={project_id}, files={file_count}, size={total_size}")
    except HTTPException:
        shutil.rmtree(extract_path, ignore_errors=True)
        raise
    except zipfile.BadZipFile:
        shutil.rmtree(extract_path, ignore_errors=True)
        raise HTTPException(status_code=400, detail="Geçersiz ZIP dosyası")
    finally:
        if os.path.exists(temp_zip):
            os.remove(temp_zip)

    return {"project_id": project_id, "path": extract_path}

@router.post("/upload/github")
async def upload_github(data: URLUpload):
    if not GITHUB_PATTERN.match(data.url.strip()):
        raise HTTPException(status_code=400, detail="Geçersiz GitHub URL'si. Sadece public repo desteklenir.")

    project_id = str(uuid.uuid4())[:8]
    clone_path = safe_path(UPLOAD_DIR, project_id)
    os.makedirs(clone_path, exist_ok=True)

    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", data.url.strip(), clone_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Git clone başarısız: {result.stderr[:200]}")

        logger.info(f"GitHub klonlandı: project_id={project_id}, url={data.url}")
    except subprocess.TimeoutExpired:
        shutil.rmtree(clone_path, ignore_errors=True)
        raise HTTPException(status_code=400, detail="Git clone zaman aşımı (60sn)")
    except HTTPException:
        shutil.rmtree(clone_path, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(clone_path, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Beklenmeyen hata: {str(e)[:100]}")

    return {"project_id": project_id, "path": clone_path}

@router.post("/upload/paste")
async def upload_paste(data: dict):
    project_id = str(uuid.uuid4())[:8]
    paste_path = safe_path(UPLOAD_DIR, project_id)
    os.makedirs(paste_path, exist_ok=True)

    code = data.get("code", "")
    if len(code.encode("utf-8")) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Kod çok büyük (max 1MB)")

    filename = sanitize_filename(data.get("filename", "paste.txt"))
    filepath = safe_path(paste_path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    logger.info(f"Kod yapıştırıldı: project_id={project_id}, filename={filename}")
    return {"project_id": project_id, "path": paste_path}