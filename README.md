# lensecode

AI Project Architect — projeni yükle, mimari/kod kalitesi/güvenlik analizini al.

## 🚀 Hızlı Başlangıç

### En kolay yol (Windows)

`start.bat` dosyasına çift tıkla. Backend + frontend'i başlatır ve tarayıcıyı açar.

İlk kurulum (bir kez):

```bat
py -m venv backend\venv
backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
copy .env.example .env
```

### Manuel

```bash
# .env oluştur ve doldur
cp .env.example .env

# Backend
cd backend
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (ayrı terminal)
cd frontend
npm install
npm run dev
```

→ Frontend: http://localhost:3000
→ Backend:  http://localhost:8000 (health: /api/health)

> Windows'ta `python` PATH'te değilse `py` komutunu veya
> `backend\venv\Scripts\python.exe` yolunu kullan.

## 🧩 Özellikler

| Özellik | Durum |
|---------|-------|
| 📦 ZIP Yükleme | ✅ |
| 🔗 GitHub Repo Klonlama | ✅ (public repo) |
| 📝 Kod Yapıştırma | ✅ |
| 🔍 Teknoloji Tespiti | ✅ |
| 🛡️ Güvenlik Analizi | ✅ (yerleşik tarayıcı) + Semgrep (opsiyonel) |
| 📊 Kod Kalitesi Puanı | ✅ |
| ❌ Eksik Özellik Tespiti | ✅ |
| ⚠️ Gereksiz Yapılanmalar | ✅ |
| 🤖 LLM Analizi | ✅ (API key varsa; yoksa fallback) |
| 📋 PDF/Markdown/JSON Rapor | ✅ |
| ✨ AI Prompt Generator | ✅ |
| 🐳 Docker / Railway Deploy | ✅ |

### Derin güvenlik taraması (Semgrep, opsiyonel)

```bash
pip install -r backend/requirements-semgrep.txt
```

Kurulu değilse backend otomatik olarak yerleşik (regex tabanlı) tarayıcıya düşer.
Kapatmak için `.env`: `ENABLE_SEMGREP=0`.

## 🔐 Güvenlik / Ortam Değişkenleri

`.env` (gitignore'da) içinde ayarlanır:

| Değişken | Açıklama |
|----------|----------|
| `LENSCODE_PASSWORD` | Giriş şifresi (zorunlu) |
| `JWT_SECRET` | Token imza anahtarı, en az 32 bayt (zorunlu) |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | LLM analizi (opsiyonel) |
| `CORS_ORIGINS` | İzinli frontend origin'leri, virgülle (boş=tümü) |
| `ENABLE_SEMGREP` | `1`/`0` |

JWT anahtarı üretmek için:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 🐳 Production (Docker)

```bash
cp .env.example .env   # değerleri doldur
docker compose build
docker compose up -d
docker compose logs -f
```

## ☁️ Railway Deploy

`.env.railway` bir şablondur; gerçek değerleri Railway dashboard > Variables
bölümünde girin. Her servis kendi `railway.json` ile Dockerfile kullanır,
portu `PORT` değişkeninden okur. Frontend servisinde `BACKEND_URL` ayarlanmalıdır.

## 🔎 SEO ve Yayın

Sitenin iki kısmı var:

| Yol | Kime açık | Ne işe yarar |
|-----|-----------|---------------|
| `/` | Herkese açık | Tanıtım sayfası — Google'ın indekslediği yer |
| `/app` | Şifre korumalı | Analiz aracı (giriş şifresi gerekir) |
| `/dashboard/[id]` | Şifre korumalı | Analiz raporu |

Yayına almadan önce `.env` (veya Railway/VPS değişkenleri) içinde
**`NEXT_PUBLIC_SITE_URL`** degerini gercek site adresiyle doldurun:

```
NEXT_PUBLIC_SITE_URL=https://siteadiniz.com
```

Bu deger `canonical`, Open Graph, Twitter kartlari, `sitemap.xml` ve
`robots.txt` icin kullanilir. Ayni degeri frontend servisine de vermeniz gerekir.

Hazir gelenler: Open Graph/Twitter meta etiketleri, dinamik paylasim goreli
(`/opengraph-image`, 1200x630 PNG), `robots.txt`, `sitemap.xml`,
`manifest.webmanifest`, favicon.

Yayindan sonra Google Search Console'a site ekleyip
`https://siteadiniz.com/sitemap.xml` gonderin.

## 📁 Proje Yapısı

```
lensecode/
├── backend/           # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/    # auth, upload, analyze, report
│   │   ├── middleware/# auth
│   │   └── services/  # tech_detector, static_analyzer, llm_analyzer, report_generator
│   ├── requirements.txt
│   └── requirements-semgrep.txt
├── frontend/          # Next.js + Tailwind
│   └── src/
│       ├── app/       # page.tsx (landing), app/page.tsx (arac), dashboard/[id]/
│       │              # robots.ts, sitemap.ts, manifest.ts, opengraph-image.tsx
│       ├── components/
│       └── lib/       # api.ts, types.ts, site.ts, useToken.ts
├── docker-compose.yml
├── nginx.conf
├── start.bat          # Windows tek tuş başlatma
└── .env.example
```
