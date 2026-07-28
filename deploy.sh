#!/bin/bash
set -e

echo "========================================"
echo "  lensecode - VPS Deployment"
echo "========================================"

SITE_NAME="${1:-lensecode}"
DOMAIN="${2:-}"

echo "[1/7] Sistem güncelleniyor..."
apt update && apt upgrade -y

echo "[2/7] Gerekli paketler kuruluyor..."
apt install -y docker.io docker-compose-v2 git curl nginx certbot python3-certbot-nginx

systemctl enable docker
systemctl start docker

echo "[3/7] Proje klonlanıyor..."
cd /opt
if [ -d "$SITE_NAME" ]; then
  cd "$SITE_NAME" && git pull
else
  git clone https://github.com/KULLANICI_ADI/lensecode.git "$SITE_NAME"
  cd "$SITE_NAME"
fi

echo "[4/7] Environment değişkenleri..."
if [ ! -f ".env" ]; then
  cp backend/.env.production .env
  echo "⚠️  .env dosyası oluşturuldu. API key'lerini ekle: nano /opt/$SITE_NAME/.env"
fi

echo "[5/7] Docker imajları build ediliyor..."
docker compose build

echo "[6/7] Servisler başlatılıyor..."
docker compose up -d

echo "[7/7] Nginx yapılandırması..."
cat > /etc/nginx/sites-available/"$SITE_NAME" <<NGINX
server {
    listen 80;
    server_name ${DOMAIN:-_};
    client_max_body_size 500M;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/"$SITE_NAME" /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

IP=$(curl -s ifconfig.me 2>/dev/null || echo "SUNUCU_IP")

echo ""
echo "========================================"
echo "  ✅ lensecode deploy tamamlandı!"
echo "========================================"
echo ""
echo "  Site: http://$IP"

if [ -n "$DOMAIN" ]; then
  echo ""
  echo "  SSL ekle: certbot --nginx -d $DOMAIN"
  echo "  Site: https://$DOMAIN"
fi

echo ""
echo "  Loglar: docker compose logs -f"
echo "  Durum:  docker compose ps"
echo "  Şifre:  .env dosyasındaki LENSCODE_PASSWORD"
echo "========================================"