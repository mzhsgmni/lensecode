import logging
import os
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import UPLOAD_DIR
from app.services.llm_analyzer import run_llm_analysis
from app.services.report_generator import generate_report
from app.services.static_analyzer import run_static_analysis
from app.services.tech_detector import detect_tech_stack

logger = logging.getLogger("lensecode")
router = APIRouter()

PROJECT_ID_PATTERN = re.compile(r"^[a-f0-9]{8}$")

class AnalyzeRequest(BaseModel):
    project_id: str

def validate_project_id(pid: str) -> str:
    if not PROJECT_ID_PATTERN.match(pid):
        raise HTTPException(status_code=400, detail="Geçersiz proje ID")
    path = os.path.realpath(os.path.join(UPLOAD_DIR, pid))
    if not path.startswith(os.path.realpath(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Geçersiz yol")
    return path

@router.post("/analyze")
async def analyze_project(req: AnalyzeRequest):
    project_path = validate_project_id(req.project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Proje bulunamadı")

    try:
        logger.info(f"Analiz başlıyor: project_id={req.project_id}")
        tech_stack = detect_tech_stack(project_path)
        static_result = run_static_analysis(project_path, tech_stack)
        llm_result = run_llm_analysis(tech_stack, static_result)

        analysis_data = {
            "project_id": req.project_id,
            "tech_stack": tech_stack,
            "static_analysis": static_result,
            "llm_analysis": llm_result,
        }

        generate_report(req.project_id, analysis_data, project_path)
        logger.info(f"Analiz tamam: project_id={req.project_id}")
        return analysis_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analiz hatası: project_id={req.project_id}, error={str(e)}")
        raise HTTPException(status_code=500, detail=f"Analiz sırasında hata: {str(e)[:100]}")