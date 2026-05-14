# DEPLOYMENT GUIDE (VPS/WSL)

## 1) Chuẩn bị
- Ubuntu/WSL có Docker + Docker Compose plugin
- Mở port phù hợp (80/443 hoặc 18080 cho demo)

## 2) Lấy source
```bash
git clone <repo-url>
cd spa-booking-django
```

## 3) Cấu hình environment
```bash
cp .env.production.example .env.production
```

Bắt buộc đổi:
- `SECRET_KEY`
- `DB_PASSWORD`
- `DB_ROOT_PASSWORD`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

## 4) Deploy
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

## 5) Verify
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
curl http://127.0.0.1:18080/api/health
```

## 6) Redeploy
```bash
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## 7) Rollback cơ bản
```bash
git log --oneline
git checkout <good-commit>
docker compose -f docker-compose.prod.yml up -d --build
```

## 8) Debug nhanh theo layer
- L4: frontend/console/network
- L3: backend logs + API response
- L2: mysql health + migrations
- L1: docker/nginx/network/port
