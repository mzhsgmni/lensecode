import os
import re
import json
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.report_generator import format_markdown, format_pdf

logger = logging.getLogger("lensecode")
router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
PROJECT_ID_PATTERN = re.compile(r"^[a-f0-9]{8}$")
ALLOWED_FORMATS = {"json", "markdown", "pdf"}

class ReportRequest(BaseModel):
    project_id: str

def validate_project_id(pid: str) -> str:
    if not PROJECT_ID_PATTERN.match(pid):
        raise HTTPException(status_code=400, detail="Geçersiz proje ID")
    path = os.path.realpath(os.path.join(UPLOAD_DIR, pid))
    if not path.startswith(os.path.realpath(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Geçersiz yol")
    return path

@router.post("/report")
async def get_report(req: ReportRequest):
    project_path = validate_project_id(req.project_id)
    report_path = os.path.join(project_path, "analysis_result.json")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Henüz analiz yapılmamış")

    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/report/{project_id}/{format}")
async def download_report(project_id: str, format: str = "json"):
    if format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Desteklenmeyen format (json/markdown/pdf)")

    project_path = validate_project_id(project_id)
    report_path = os.path.join(project_path, "analysis_result.json")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Rapor bulunamadı")

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if format == "json":
        from fastapi.responses import JSONResponse
        return JSONResponse(content=data)
    elif format == "markdown":
        from fastapi.responses import PlainTextResponse
        md = format_markdown(data)
        return PlainTextResponse(content=md, media_type="text/markdown")
    elif format == "pdf":
        pdf_path = format_pdf(data, project_id)
        if not pdf_path:
            raise HTTPException(status_code=500, detail="PDF oluşturulamadı")
        from fastapi.responses import FileResponse
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"{project_id}_rapor.pdf")