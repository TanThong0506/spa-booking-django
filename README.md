# Spa Booking Django — DevOps Project

Hệ thống đặt lịch spa đầy đủ theo hướng production: Backend API, Frontend (Django templates), Database, Docker, CI/CD và tài liệu debug theo layer.

## 1) Kiến trúc hệ thống

- Frontend: Django templates + static assets
- Backend: Django + Django REST Framework
- Database: MySQL 8
- Reverse Proxy: Nginx
- Runtime: Gunicorn
- CI: GitHub Actions (lint, test, build)

Chi tiết sơ đồ và luồng CI/CD: xem `docs/DEVOPS_PROJECT_REPORT.md`.

## 2) Tính năng chính

- Đăng ký/đăng nhập
- Danh sách dịch vụ
- Đặt lịch và quản lý lịch hẹn
- Dashboard thống kê
- API health check: `/api/health` và `/api/health/`

## 3) Yêu cầu DevOps đã đáp ứng

- Dockerfile (multi-stage) + `docker-compose.yml` + `docker-compose.prod.yml`
- Có `.env.example` và `.env.production.example`
- Không commit `.env`
- GitHub Actions gồm `lint` + `test` + `build`
- Trigger pipeline khi `push` và `pull_request`
- Có tài liệu incident (>=3 lỗi) theo Layer Thinking

## 4) Chạy local nhanh

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set DB_ENGINE=sqlite
python manage.py migrate
python manage.py runserver
```

## 5) Chạy bằng Docker (demo bắt buộc)

### Development stack
```bash
docker compose up -d --build
docker compose ps
docker compose logs -f web
```

### Production-like stack
```bash
copy .env.production.example .env.production
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f nginx
```

## 6) API test nhanh

```bash
curl http://127.0.0.1:8000/api/health
```

Hoặc chạy script:

```bash
python test_api.py
```

## 7) CI/CD

Workflow: `.github/workflows/django_ci.yml`

Gồm 3 job:
- `lint`: flake8
- `test`: Django test + check
- `build`: docker build + deploy sanity check

## 8) Tài liệu đồ án

- Báo cáo DevOps đầy đủ: `docs/DEVOPS_PROJECT_REPORT.md`
- Incident report (3 sự cố): `docs/INCIDENT_REPORT.md`
- Deployment/redeploy guide: `docs/DEPLOYMENT_GUIDE.md`

## 9) Lưu ý bảo mật

- Không dùng `ALLOWED_HOSTS=*` trên production.
- Luôn đổi `SECRET_KEY`, `DB_PASSWORD`, `DB_ROOT_PASSWORD` trước deploy.
- Không commit file `.env`, `.env.local`, `.env.production` chứa giá trị thật.