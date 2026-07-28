import os
import subprocess
import json
from typing import Dict, Any, List

EXCLUDE_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", ".next", "coverage"}

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
                except:
                    pass
    return total_files, total_lines

def run_semgrep(project_path: str) -> List[Dict[str, Any]]:
    issues = []
    try:
        result = subprocess.run(
            ["semgrep", "--json", "--config=auto", project_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for r in data.get("results", []):
                issues.append({
                    "severity": r.get("extra", {}).get("severity", "medium"),
                    "type": r.get("check_id", "unknown"),
                    "description": r.get("extra", {}).get("message", ""),
                    "file": r.get("path", ""),
                })
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return issues

def check_unused_packages(project_path: str) -> List[str]:
    unused = []
    pkg_json = os.path.join(project_path, "package.json")
    if not os.path.exists(pkg_json):
        return unused

    try:
        with open(pkg_json, "r", encoding="utf-8") as f:
            pkg = json.load(f)

        all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        for dep in all_deps:
            found = False
            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                        fp = os.path.join(root, file)
                        try:
                            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                                content = fh.read()
                                if dep in content or dep.replace("@", "").replace("/", "") in content:
                                    found = True
                                    break
                        except:
                            pass
                if found:
                    break
            if not found:
                unused.append(dep)
    except:
        pass

    return unused

def check_missing_features(pkg: dict, files: list) -> List[str]:
    missing = []
    all_content = " ".join(files)

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

def check_redundant_features(pkg: dict, files: list) -> List[str]:
    redundant = []
    all_content = " ".join(files)

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

def run_static_analysis(project_path: str, tech_stack: dict) -> dict:
    total_files, total_lines = count_files_and_lines(project_path)
    security_issues = run_semgrep(project_path)
    unused_packages = check_unused_packages(project_path)

    all_files_content = []
    for root, _, files in os.walk(project_path):
        for file in files:
            fp = os.path.join(root, file)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    all_files_content.append(fh.read())
            except:
                pass

    pkg = {}
    pkg_json = os.path.join(project_path, "package.json")
    if os.path.exists(pkg_json):
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
        except:
            pass

    missing_features = check_missing_features(pkg, all_files_content)
    redundant_features = check_redundant_features(pkg, all_files_content)

    code_quality_score = 100
    code_quality_score -= len(unused_packages) * 3
    code_quality_score -= len(security_issues) * 5
    code_quality_score -= len(redundant_features) * 5
    code_quality_score = max(0, min(100, code_quality_score))

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "security_issues": security_issues,
        "unused_packages": unused_packages,
        "missing_features": missing_features,
        "redundant_features": redundant_features,
        "code_quality_score": code_quality_score,
    }