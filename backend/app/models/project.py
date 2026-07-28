from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class TechStack(BaseModel):
    framework: Optional[str] = None
    language: Optional[str] = None
    database: Optional[str] = None
    ui_library: Optional[str] = None
    css_framework: Optional[str] = None
    authentication: Optional[str] = None
    packages: List[str] = []

class SecurityIssue(BaseModel):
    severity: str  # critical / high / medium / low
    type: str
    description: str
    file: Optional[str] = None

class StaticAnalysisResult(BaseModel):
    total_files: int
    total_lines: int
    tech_stack: Dict[str, Any]
    security_issues: List[SecurityIssue] = []
    code_quality_score: Optional[int] = None
    unused_packages: List[str] = []
    missing_features: List[str] = []
    redundant_features: List[str] = []

class LLMAnalysisResult(BaseModel):
    overall_score: int
    code_quality: int
    architecture: int
    performance: int
    security: int
    summary: str
    ai_mistakes: List[str] = []
    recommendations: List[str] = []
    roadmap: List[str] = []
    prompt_generator: Optional[str] = None

class AnalysisResult(BaseModel):
    project_id: str
    status: str = "completed"
    tech_stack: Dict[str, Any]
    static_analysis: Dict[str, Any]
    llm_analysis: Dict[str, Any]