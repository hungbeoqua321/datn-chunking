#!/bin/bash
# Cài web đồ án lên VPS: systemd (uvicorn + llama-server) + nginx site + chứng chỉ Let's Encrypt.
# Không đụng tới các site nginx khác; trước/sau khi reload in mã trả về của chúng để đối chiếu.
#   sudo deploy/cai-dat.sh
set -euo pipefail
cd "$(dirname "$0")/.."
GOC="$(pwd)"
DATN_HOST="$(grep -E '^DATN_HOST=' .env | cut -d= -f2-)"
kiem() { for h in em.134-185-85-25.sslip.io bienban.134-185-85-25.sslip.io 134-185-85-25.sslip.io bantincophieu.com www.bantincophieu.com; do
  printf "  %-36s %s\n" "$h" "$(curl -s -o /dev/null -m 20 -w '%{http_code}' https://$h/ || echo lỗi)"; done; }
echo "== các site cũ TRƯỚC khi cài"; kiem
install -m 644 deploy/datn-web.service /etc/systemd/system/datn-web.service
install -m 644 deploy/datn-llm.service /etc/systemd/system/datn-llm.service
systemctl daemon-reload
systemctl enable --now datn-llm datn-web
deploy/render.sh > /etc/nginx/sites-available/datn
ln -sf /etc/nginx/sites-available/datn /etc/nginx/sites-enabled/datn
nginx -t && systemctl reload nginx
certbot --nginx -d "$DATN_HOST" --redirect --non-interactive --agree-tos --keep-until-expiring --register-unsafely-without-email
nginx -t && systemctl reload nginx
echo "== các site cũ SAU khi cài"; kiem
echo "== web đồ án"; curl -s -m 20 "https://$DATN_HOST/healthz"; echo
