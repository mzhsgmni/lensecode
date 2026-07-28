import os
import json

FRAMEWORK_SIGNATURES = {
    "next.config": "Next.js",
    "next.config.js": "Next.js",
    "next.config.ts": "Next.js",
    "nuxt.config": "Nuxt.js",
    "vite.config": "Vite",
    "angular.json": "Angular",
    "vue.config": "Vue.js",
    "svelte.config": "Svelte",
    "remix.config": "Remix",
    "gatsby-config": "Gatsby",
    "astro.config": "Astro",
    "package.json": None,
}

LANG_EXTENSIONS = {
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".js": "JavaScript",
    ".jsx": "JavaScript (React)",
    ".py": "Python",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
}

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def detect_tech_stack(project_path: str) -> dict:
    result = {
        "framework": None,
        "language": None,
        "database": None,
        "ui_library": None,
        "css_framework": None,
        "authentication": None,
        "packages": [],
        "dev_packages": [],
    }

    root_files = os.listdir(project_path)
    for f in root_files:
        if f in FRAMEWORK_SIGNATURES and FRAMEWORK_SIGNATURES[f]:
            result["framework"] = FRAMEWORK_SIGNATURES[f]
            break

    pkg_json_path = os.path.join(project_path, "package.json")
    pkg = read_json(pkg_json_path)
    if pkg:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        result["packages"] = list(deps.keys())

        if "next" in deps:
            result["framework"] = "Next.js"
        elif "nuxt" in deps:
            result["framework"] = "Nuxt.js"
        elif "react" in deps:
            result["framework"] = "React"
        elif "vue" in deps:
            result["framework"] = "Vue.js"
        elif "svelte" in deps:
            result["framework"] = "Svelte"

        if "typescript" in deps or "typescript" in pkg.get("devDependencies", {}):
            result["language"] = "TypeScript"
        else:
            result["language"] = "JavaScript"

        if "prisma" in deps:
            result["database"] = "Prisma + PostgreSQL"
        elif "mongoose" in deps or "mongodb" in deps:
            result["database"] = "MongoDB"
        elif "typeorm" in deps:
            result["database"] = "TypeORM"
        elif "drizzle-orm" in deps:
            result["database"] = "Drizzle ORM"

        if "tailwindcss" in deps or "tailwindcss" in pkg.get("devDependencies", {}):
            result["css_framework"] = "TailwindCSS"
        elif "bootstrap" in deps:
            result["css_framework"] = "Bootstrap"
        elif "@chakra-ui" in deps or "@mui/material" in deps:
            result["css_framework"] = "Material UI"

        if "next-auth" in deps or "next-auth" in pkg.get("devDependencies", {}):
            result["authentication"] = "NextAuth"
        elif "firebase" in deps:
            result["authentication"] = "Firebase Auth"
        elif "clerk" in deps or "@clerk" in deps:
            result["authentication"] = "Clerk"
        elif "auth0" in deps:
            result["authentication"] = "Auth0"

    req_txt = os.path.join(project_path, "requirements.txt")
    if os.path.exists(req_txt):
        with open(req_txt, "r", encoding="utf-8") as f:
            for line in f:
                pkg_name = line.split("==")[0].split(">=")[0].strip().lower()
                if pkg_name:
                    result["packages"].append(pkg_name)
                    if "fastapi" == pkg_name:
                        result["framework"] = "FastAPI"
                    elif "django" == pkg_name:
                        result["framework"] = "Django"
                    elif "flask" == pkg_name:
                        result["framework"] = "Flask"
                    elif "sqlalchemy" in pkg_name:
                        result["database"] = "SQLAlchemy"
                    elif "psycopg2" in pkg_name or "asyncpg" in pkg_name:
                        result["database"] = "PostgreSQL"

    if not result["language"]:
        ext_count = {}
        for root, _, files in os.walk(project_path):
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in LANG_EXTENSIONS:
                    ext_count[ext] = ext_count.get(ext, 0) + 1
        if ext_count:
            main_ext = max(ext_count, key=ext_count.get)
            result["language"] = LANG_EXTENSIONS[main_ext]

    return result