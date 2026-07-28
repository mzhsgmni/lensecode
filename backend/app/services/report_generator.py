import json
import os
import re
from typing import Any

from app.config import UPLOAD_DIR

_TR_MAP = {"ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I",
           "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U"}
_TR_MAP_RE = re.compile("|".join(map(re.escape, _TR_MAP)))
_SAFE_CHARS = set(chr(c) for c in range(32, 127)) | set("\n\r\t") | set(_TR_MAP.values())

def generate_report(project_id: str, analysis_data: dict, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "analysis_result.json")

    score = analysis_data.get("llm_analysis", {})
    static = analysis_data.get("static_analysis", {})

    report = {
        "project_id": project_id,
        "overall_score": score.get("overall_score", 0),
        "categories": {
            "code_quality": {"score": score.get("code_quality", 0), "icon": "📝"},
            "architecture": {"score": score.get("architecture", 0), "icon": "🏗️"},
            "performance": {"score": score.get("performance", 0), "icon": "⚡"},
            "security": {"score": score.get("security", 0), "icon": "🛡️"},
        },
        "tech_stack": analysis_data.get("tech_stack", {}),
        "stats": {
            "total_files": static.get("total_files", 0),
            "total_lines": static.get("total_lines", 0),
        },
        "security_issues": static.get("security_issues", []),
        "security_scan": static.get("security_scan", {}),
        "unused_packages": static.get("unused_packages", []),
        "missing_features": static.get("missing_features", []),
        "redundant_features": static.get("redundant_features", []),
        "ai_mistakes": score.get("ai_mistakes", []),
        "recommendations": score.get("recommendations", []),
        "roadmap": score.get("roadmap", []),
        "summary": score.get("summary", ""),
        "prompt_generator": score.get("prompt_generator", ""),
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report_path

def format_markdown(data: dict) -> str:
    lines = []
    lines.append(f"# lensecode Analiz Raporu\n")
    lines.append(f"**Proje ID:** {data.get('project_id', '—')}\n")
    lines.append(f"**Genel Puan:** {data.get('overall_score', '—')}/100\n")

    lines.append("## 📊 Kategori Puanları\n")
    for name, cat in data.get("categories", {}).items():
        bar = "🟩" * (cat["score"] // 10) + "⬜" * (10 - cat["score"] // 10)
        lines.append(f"- {cat['icon']} **{name.replace('_', ' ').title()}:** {cat['score']}/100 {bar}")

    lines.append("\n## 🔧 Teknoloji Yığını\n")
    for key, val in data.get("tech_stack", {}).items():
        if val:
            if isinstance(val, list):
                lines.append(f"- **{key.replace('_', ' ').title()}:** {', '.join(val[:10])}")
            else:
                lines.append(f"- **{key.replace('_', ' ').title()}:** {val}")

    if data.get("security_issues"):
        lines.append("\n## 🛡️ Güvenlik Sorunları\n")
        for issue in data["security_issues"][:10]:
            sev = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(issue.get("severity", "medium"), "⚪")
            lines.append(f"- {sev} {issue.get('description', '')} ({issue.get('file', '')})")

    if data.get("missing_features"):
        lines.append("\n## ❌ Eksik Özellikler\n")
        for feat in data["missing_features"]:
            lines.append(f"- ❌ {feat}")

    if data.get("redundant_features"):
        lines.append("\n## ⚠️ Gereksiz Yapılanmalar\n")
        for feat in data["redundant_features"]:
            lines.append(f"- ⚠️ {feat}")

    if data.get("recommendations"):
        lines.append("\n## 💡 Öneriler\n")
        for rec in data["recommendations"]:
            lines.append(f"- {rec}")

    if data.get("roadmap"):
        lines.append("\n## 🗺️ Yol Haritası\n")
        for i, step in enumerate(data["roadmap"], 1):
            lines.append(f"{i}. {step}")

    if data.get("prompt_generator"):
        lines.append("\n## ✨ AI Prompt\n")
        lines.append(f"```\n{data['prompt_generator']}\n```")

    return "\n".join(lines)

def pdf_safe(text: Any) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = _TR_MAP_RE.sub(lambda m: _TR_MAP[m.group()], text)
    return "".join(ch for ch in text if ch in _SAFE_CHARS)


def format_pdf(data: dict, project_id: str) -> str:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    W = pdf.w - pdf.l_margin - pdf.r_margin

    def line(text: str, style: str = "", size: int = 11, gap: int = 0, align: str = "L"):
        pdf.set_font("Arial", style, size)
        pdf.set_x(pdf.l_margin)
        pdf.cell(W, 6, pdf_safe(text), new_x="LMARGIN", new_y="NEXT", align=align)
        if gap:
            pdf.ln(gap)

    def para(text: str, size: int = 11):
        clean = pdf_safe(text).strip()
        if not clean:
            return
        pdf.set_font("Arial", "", size)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 6, clean)

    line("lensecode - Analiz Raporu", "B", 20, gap=2, align="C")
    line(f"Proje: {project_id}", "", 12, gap=10, align="C")
    line(f"Genel Puan: {data.get('overall_score', '-')}/100", "B", 16, gap=6)

    for name, cat in data.get("categories", {}).items():
        line(f"{name.replace('_', ' ').title()}: {cat['score']}/100", "", 12)

    sections = (
        ("Ozet", data.get("summary")),
        ("Eksik Ozellikler", data.get("missing_features")),
        ("Gereksiz Yapilanmalar", data.get("redundant_features")),
        ("Kullanilmayan Paketler", data.get("unused_packages")),
        ("Guvenlik Sorunlari", [f"[{i.get('severity', '?')}] {i.get('description', '')}" for i in data.get("security_issues", [])]),
        ("Oneriler", data.get("recommendations")),
        ("Yol Haritasi", [f"{n}. {s}" for n, s in enumerate(data.get("roadmap", []), 1)]),
        ("AI Prompt", data.get("prompt_generator")),
    )

    for title, content in sections:
        if not content:
            continue
        pdf.ln(8)
        line(title, "B", 13, gap=2)
        items = [content] if isinstance(content, str) else list(content)
        for item in items:
            para(item)

    output_path = os.path.join(UPLOAD_DIR, project_id, "rapor.pdf")
    pdf.output(output_path)
    return output_path