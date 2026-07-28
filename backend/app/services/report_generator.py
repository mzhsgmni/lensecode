import json
import os
from typing import Dict, Any

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

def format_pdf(data: dict, project_id: str) -> str:
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, f"lensecode - Analiz Raporu", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Proje: {project_id}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Genel Puan: {data.get('overall_score', '—')}/100", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        for name, cat in data.get("categories", {}).items():
            pdf.set_font("Arial", "", 12)
            label = name.replace("_", " ").title()
            pdf.cell(0, 8, f"{cat.get('icon', '')} {label}: {cat['score']}/100", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)
        if data.get("summary"):
            pdf.set_font("Arial", "I", 11)
            pdf.multi_cell(0, 6, f"Ozet: {data['summary']}")

        output_path = os.path.join(os.path.dirname(__file__), "..", "uploads", project_id, "rapor.pdf")
        pdf.output(output_path)
        return output_path
    except ImportError:
        return None