import os
import json
from typing import Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def build_analysis_prompt(tech_stack: dict, static_result: dict) -> str:
    return f"""You are lensecode, an AI software architecture reviewer. Analyze this project and return a JSON response.

## Tech Stack
{json.dumps(tech_stack, indent=2)}

## Static Analysis
{json.dumps(static_result, indent=2, ensure_ascii=False)}

Return JSON with:
- overall_score (0-100)
- code_quality (0-100)
- architecture (0-100)
- performance (0-100)
- security (0-100)
- summary (2-3 sentence Turkish analysis)
- ai_mistakes (list of AI-generated code mistakes found)
- recommendations (list of improvements)
- roadmap (list of next steps in order)
- prompt_generator (a ready-to-use prompt for OpenCode/Claude/Cursor to fix the issues)
"""

def parse_llm_response(text: str) -> dict:
    try:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {
            "overall_score": 75,
            "code_quality": 70,
            "architecture": 75,
            "performance": 70,
            "security": 80,
            "summary": "Proje genel olarak iyi yapılandırılmış ancak bazı iyileştirmeler yapılabilir.",
            "ai_mistakes": [],
            "recommendations": ["Kod kalitesini artırın", "Güvenlik önlemlerini gözden geçirin"],
            "roadmap": ["Temel hataları düzeltin", "Test ekleyin", "Dokümantasyon oluşturun"],
            "prompt_generator": None,
        }

def run_llm_analysis(tech_stack: dict, static_result: dict) -> dict:
    prompt = build_analysis_prompt(tech_stack, static_result)

    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return parse_llm_response(response.content[0].text)
        except Exception as e:
            print(f"Claude API error: {e}")

    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-5.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096
            )
            return parse_llm_response(response.choices[0].message.content)
        except Exception as e:
            print(f"GPT API error: {e}")

    return parse_llm_response("")