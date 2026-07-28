# lensecode

## 🚀 Hızlı Başlangıç

### Development (Yerel)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (ayrı terminal)
cd frontend
npm install
npm run dev
```

→ Frontend: http://localhost:3000
→ Backend:  http://localhost:8000

### Production (Docker)

```bash
# .env dosyasını oluştur
cp .env.example .env
# API key'lerini ekle

# Build ve başlat
docker compose build
docker compose up -d

# Logları izle
docker compose logs -f
```

### VPS Deploy

```bash
# VPS'e bağlan ve scripti çalıştır
curl -fsSL https://raw.githubusercontent.com/KULLANICI/lensecode/main/deploy.sh | bash
```

## 🧩 MVP Özellikleri

| Özellik | Durum |
|---------|-------|
| 📦 ZIP Yükleme | ✅ |
| 🔗 GitHub Repo Klonlama | ✅ |
| 📝 Kod Yapıştırma | ✅ |
| 🔍 Teknoloji Tespiti | ✅ |
| 🛡️ Güvenlik Analizi | ✅ (Semgrep) |
| 📊 Kod Kalitesi Puanı | ✅ |
| ❌ Eksik Özellik Tespiti | ✅ |
| ⚠️ Gereksiz Yapılanmalar | ✅ |
| 🤖 LLM Analizi (Claude + GPT) | ✅ (API key gerekli) |
| 📋 PDF/Markdown Rapor | ✅ |
| ✨ AI Prompt Generator | ✅ |
| 🐳 Docker Deploy | ✅ |
| 🌐 VPS Deploy Script | ✅ |

## 📁 Proje Yapısı

```
lensecode/
├── backend/           # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/    # upload, analyze, report
│   │   ├── services/  # tech_detector, static_analyzer, llm_analyzer, report_generator
│   │   └── models/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          # Next.js + Tailwind
│   ├── src/
│   │   ├── app/       # page.tsx, dashboard/[id]/page.tsx
│   │   └── components/ # FileUploader, ScoreCard, AnalysisChart, ReportView, PromptGenerator
│   ├── Dockerfile
│   └── next.config.ts
├── docker-compose.yml
├── nginx.conf
├── deploy.sh
└── .env.example
```