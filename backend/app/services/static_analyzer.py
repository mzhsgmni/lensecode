import json
import os
import re
import shutil
import subprocess
from typing import Any, Dict, List

from app.config import ENABLE_SEMGREP, SEMGREP_CONFIG

EXCLUDE_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", ".next", "coverage"}

SECRET_PATTERNS = [
    (r"(?i)\b(?:api[_-]?|secret[_-]?|private[_-]?|client[_-]?|app[_-]?|auth[_-]?|encryption[_-]?)?(?:key|token|passw[or]d|passwd|pwd|secret|credential)s?\b\s*[:=]\s*['\"][^'\"\s]{6,}['\"]",
     "hardcoded-credentials", "Kod içinde sabitlenmiş kimlik bilgisi", "high"),
    (r"AKIA[0-9A-Z]{16}", "aws-access-key", "AWS erişim anahtarı kodda gömülü", "critical"),
    (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----", "private-key", "Özel anahtar içeriği kodda gömülü", "critical"),
    (r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}", "openai-api-key", "OpenAI API anahtarı kodda gömülü", "critical"),
    (r"\bsk_live_[A-Za-z0-9]{16,}", "stripe-key", "Stripe canlı anahtarı kodda gömülü", "critical"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "github-token", "GitHub token'ı kodda gömülü", "critical"),
    (r"\bAIza[0-9A-Za-z_-]{30,}", "google-api-key", "Google API anahtarı kodda gömülü", "critical"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}", "slack-token", "Slack token'ı kodda gömülü", "high"),
    (r"(?i)\beval\s*\(", "eval-usage", "eval() kullanımı — kod çalıştırma riski", "high"),
    (r"\bnew\s+Function\s*\(", "dynamic-code", "new Function() ile dinamik kod üretimi", "high"),
    (r"\bexec\s*\(\s*(?:os\.system|subprocess)", "shell-exec", "Kabuk komutu çalıştırma", "high"),
    (r"(?i)child_process\s*\.\s*exec|shell\s*=\s*True", "shell-exec", "Kabuk kabuğu (shell=True) kullanımı", "high"),
    (r"(?i)\bmd5\s*\(|hashlib\.md5", "weak-hash", "Kırılgan karma algoritması (MD5)", "medium"),
    (r"(?i)\bsha1\s*\(", "weak-hash", "Kırılgan karma algoritması (SHA-1)", "medium"),
    (r"(?i)verify\s*=\s*False|rejectUnauthorized\s*:\s*false", "tls-verify-disabled", "TLS/SSL doğrulaması kapatılmış", "high"),
    (r"(?i)\.innerHTML\s*=|dangerouslySetInnerHTML", "xss-innerhtml", "innerHTML kullanımı — XSS riski", "medium"),
    (r"(?i)\bhttp://(?!localhost|127\.0\.0\.1)[a-z0-9.-]+\.[a-z]{2,}", "insecure-http", "Güvensiz HTTP bağlantısı", "low"),
]

COMPILED_SECRET_PATTERNS = [(re.compile(p), cid, desc, sev) for p, cid, desc, sev in SECRET_PATTERNS]
SOURCE_EXTENSIONS = (".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".java", ".php", ".rb", ".rs", ".env", ".yml", ".yaml", ".json", ".sql")


def count_files_and_lines(project_path: str) -> tuple:
    total_files = 0
    total_lines = 0
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in (".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".rs", ".java", ".css", ".scss", ".html", ".json", ".yml", ".yaml", ".md", ".sql"):
                total_files += 1
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                        total_lines += sum(1 for _ in fh)
                except OSError:
                    pass
    return total_files, total_lines


def run_builtin_secret_scan(project_path: str) -> List[Dict[str, Any]]:
    issues = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if os.path.splitext(f)[1] not in SOURCE_EXTENSIONS:
                continue
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except OSError:
                continue
            for lineno, line in enumerate(content.splitlines(), 1):
                if len(line) > 500:
                    continue
                for pattern, check_id, desc, severity in COMPILED_SECRET_PATTERNS:
                    if pattern.search(line):
                        issues.append({
                            "severity": severity,
                            "type": check_id,
                            "description": f"{desc} (satır {lineno})",
                            "file": os.path.relpath(fp, project_path),
                        })
    return issues


def run_semgrep(project_path: str) -> Dict[str, Any]:
    if not ENABLE_SEMGREP:
        return {"available": False, "reason": "ENABLE_SEMGREP=0", "issues": []}

    if shutil.which("semgrep") is None:
        return {"available": False, "reason": "semgrep yuklu degil", "issues": []}

    try:
        result = subprocess.run(
            ["semgrep", "--json", f"--config={SEMGREP_CONFIG}", "--quiet", project_path],
            capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        return {"available": False, "reason": "semgrep 120sn zaman asimi", "issues": []}

    if result.returncode != 0:
        return {"available": False, "reason": (result.stderr or "semgrep basarisiz")[:200], "issues": []}

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"available": False, "reason": "semgrep ciktisi okunamadi", "issues": []}

    issues = [
        {
            "severity": r.get("extra", {}).get("severity", "medium"),
            "type": r.get("check_id", "unknown"),
            "description": r.get("extra", {}).get("message", ""),
            "file": r.get("path", ""),
        }
        for r in data.get("results", [])
    ]
    return {"available": True, "reason": "", "issues": issues}


def check_unused_packages(project_path: str) -> List[str]:
    unused = []
    pkg_json = os.path.join(project_path, "package.json")
    if not os.path.exists(pkg_json):
        return unused

    try:
        with open(pkg_json, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return unused

    all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    if not all_deps:
        return unused

    haystack = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as fh:
                        haystack.append(fh.read())
                except OSError:
                    pass

    all_content = "\n".join(haystack)
    if not all_content:
        return []

    for dep in all_deps:
        if dep in all_content or dep.replace("@", "").replace("/", "") in all_content:
            continue
        unused.append(dep)

    return unused

def check_missing_features(all_content: str) -> List[str]:
    missing = []

    essential = [
        ("forgot_password|reset-password|ForgotPassword", "Forgot Password"),
        ("verify-email|email-verification|EmailVerification", "Email Verification"),
        ("2fa|two-factor|mfa", "2FA"),
        ("rate.llimit|rate_limit|RateLimit", "Rate Limit"),
        ("audit.log|audit_log|AuditLog", "Audit Log"),
        ("health|/api/health", "Health Check"),
        ("test|spec|jest|pytest", "Unit Tests"),
        ("docker-compose|Dockerfile", "Docker"),
        (".env.example|.env", "Environment Config"),
        ("error.boundary|ErrorBoundary|error_handler", "Error Handling"),
        ("loading|skeleton|spinner", "Loading States"),
        ("404|not-found|NotFound", "404 Page"),
    ]

    for pattern, name in essential:
        import re
        if not re.search(pattern, all_content, re.IGNORECASE):
            missing.append(name)

    return missing

def check_redundant_features(all_content: str) -> List[str]:
    redundant = []

    ui_libs = ["@mui/material", "@chakra-ui/react", "@radix-ui", "antd", "ant-design", "bootstrap", "react-bootstrap", "tailwindcss"]
    found_ui = [lib for lib in ui_libs if lib in all_content]
    if len(found_ui) > 1:
        redundant.append(f"Birden çok UI kütüphanesi: {', '.join(found_ui[:3])}")

    state_libs = ["redux", "mobx", "recoil", "zustand", "jotai", "valtio"]
    found_state = [lib for lib in state_libs if lib in all_content]
    if len(found_state) > 1:
        redundant.append(f"Birden çok state management: {', '.join(found_state[:3])}")

    auth_libs = ["next-auth", "firebase/auth", "@clerk", "auth0"]
    found_auth = [lib for lib in auth_libs if lib in all_content]
    if len(found_auth) > 1:
        redundant.append(f"Birden çok auth sistemi: {', '.join(found_auth[:3])}")

    return redundant

def collect_source_text(project_path: str) -> str:
    chunks = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if os.path.getsize(os.path.join(root, file)) > 1_000_000:
                continue
            try:
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as fh:
                    chunks.append(fh.read())
            except OSError:
                pass
    return "\n".join(chunks)


def run_static_analysis(project_path: str, tech_stack: dict) -> dict:
    total_files, total_lines = count_files_and_lines(project_path)
    semgrep_result = run_semgrep(project_path)

    security_issues = list(semgrep_result["issues"])
    seen = {(i["type"], i["file"], i["description"]) for i in security_issues}
    for issue in run_builtin_secret_scan(project_path):
        key = (issue["type"], issue["file"], issue["description"])
        if key not in seen:
            seen.add(key)
            security_issues.append(issue)

    unused_packages = check_unused_packages(project_path)
    all_content = collect_source_text(project_path)

    missing_features = check_missing_features(all_content)
    redundant_features = check_redundant_features(all_content)

    severity_penalty = {"critical": 15, "high": 8, "medium": 3, "low": 1}
    code_quality_score = 100
    code_quality_score -= len(unused_packages) * 3
    code_quality_score -= len(redundant_features) * 5
    code_quality_score -= sum(severity_penalty.get(i.get("severity", "medium"), 3) for i in security_issues)
    code_quality_score = max(0, min(100, code_quality_score))

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "security_issues": security_issues,
        "security_scan": {
            "semgrep_available": semgrep_result["available"],
            "semgrep_reason": semgrep_result["reason"],
            "builtin_scan": True,
        },
        "unused_packages": unused_packages,
        "missing_features": missing_features,
        "redundant_features": redundant_features,
        "code_quality_score": code_quality_score,
    }