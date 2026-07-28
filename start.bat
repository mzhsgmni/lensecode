@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   lensecode - yerel baslatma
echo ============================================
echo.

if not exist "backend\venv\Scripts\python.exe" (
  echo [HATA] backend\venv bulunamadi.
  echo.
  echo Once su komutlari calistirin ^(bir kez^):
  echo   py -m venv backend\venv
  echo   backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
  echo.
  pause
  exit /b 1
)

if not exist ".env" (
  echo [BILGI] .env bulunamadi, .env.example kopyalaniyor...
  copy /Y ".env.example" ".env" >nul
  echo [UYARI] .env icindeki LENSCODE_PASSWORD ve JWT_SECRET degerlerini doldurun!
  echo.
)

if not exist "frontend\node_modules" (
  echo [BILGI] frontend bagimliliklari kuruluyor ^(biraz surebilir^)...
  pushd frontend
  call npm install
  popd
  echo.
)

echo [BILGI] Backend baslatiliyor  -^> http://localhost:8000
start "lensecode backend" /D "%~dp0backend" cmd /k "venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [BILGI] Frontend baslatiliyor -^> http://localhost:3000
start "lensecode frontend" /D "%~dp0frontend" cmd /k "npm run dev"

echo.
echo [BILGI] Servislerin acilmasi bekleniyor...
timeout /t 10 /nobreak >nul
start "" "http://localhost:3000"

echo.
echo ============================================
echo   Hazir!  http://localhost:3000
echo   Kapatmak icin acilan iki pencereyi kapatin.
echo ============================================
endlocal
