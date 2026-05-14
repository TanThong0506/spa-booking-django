# DEVOPS PROJECT REPORT — SPA BOOKING

## 1. Mục tiêu hoàn thành
Dự án đã hoàn thiện theo tiêu chí DevOps:
- Hệ thống chạy được theo mô hình production (web + db + nginx)
- Triển khai được bằng Docker Compose
- Có pipeline CI (lint, test, build)
- Có quy trình debug theo layer
- Có tài liệu incident thực tế

## 2. Kiến trúc bắt buộc
- **Frontend:** Django Template UI (tương đương frontend layer)
- **Backend API:** Django REST Framework
- **Database:** MySQL 8
- **Reverse proxy:** Nginx
- **Application server:** Gunicorn

Luồng request:
`Client -> Nginx -> Django(Gunicorn) -> MySQL`

## 3. Phân vai nhóm (5 người)
### (1) Backend Engineer
- Xây dựng API và model DB
- Endpoint health: `/api/health`
- Có logging khi lỗi qua `logger.exception`

### (2) Frontend Engineer
- Xây dựng UI qua Django templates
- Tách giao diện và backend route rõ ràng
- Không hardcode secret trong frontend

### (3) DevOps Engineer (CI/CD Owner)
- Thiết lập GitHub Actions:
  - lint
  - test
  - build
- Trigger: push, pull_request
- Pipeline fail khi có lỗi

### (4) Infrastructure Engineer (Deploy Owner)
- Thiết kế deployment bằng Docker Compose
- Triển khai được trên VPS/WSL/Cloud VM theo hướng dẫn
- Có quy trình redeploy

### (5) QA/SRE Engineer
- Test API, test container
- Phân tích incident theo layer
- Viết tài liệu postmortem

## 4. Docker bắt buộc
### Thành phần
- `Dockerfile` (multi-stage build)
- `docker-compose.yml` (dev stack)
- `docker-compose.prod.yml` (production-like stack)

### Lệnh demo
```bash
docker compose up -d --build
docker compose ps
docker compose logs -f web
```

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f nginx
```

## 5. Git & Branching
Đang sử dụng:
- `main`
- `develop` (dev)
- `feature/*` (ví dụ: `feature/api-finalize`, `feature/admin-redesign`)

Đáp ứng yêu cầu branching strategy.

## 6. Environment & cấu hình
- Có `.env.example`
- Có `.env.production.example`
- `.env` không commit
- Không hardcode DB credentials trong compose chính

## 7. CI (Continuous Integration)
File: `.github/workflows/django_ci.yml`

Pipeline gồm:
1. Install dependencies
2. Lint (`flake8`)
3. Test (`python manage.py test`)
4. Build (`docker build` + Django deploy sanity check)

Trigger:
- Push mọi branch
- Pull request mọi branch

## 8. CD / Deploy
### Môi trường mục tiêu
- WSL Ubuntu / VPS Docker / Cloud VM

### Thứ tự deploy chuẩn
1. Cập nhật biến môi trường
2. Deploy backend + database
3. Deploy nginx/frontend route
4. Kiểm tra CORS, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS

### Redeploy
```bash
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## 9. Logging & Debug theo layer
- **L4 Frontend:** lỗi UI/JS/HTTP
- **L3 Backend:** Django log, Gunicorn log, API response
- **L2 External:** MySQL connection, auth, migration
- **L1 Infrastructure:** container/network/nginx/port

Xem báo cáo sự cố: `docs/INCIDENT_REPORT.md`.

## 10. Checklist demo nhanh
### System
- [ ] Frontend load được
- [ ] Không lỗi console
- [ ] `/api/health` trả OK
- [ ] API trả dữ liệu

### Docker
- [ ] Có Dockerfile
- [ ] Có docker-compose
- [ ] `docker compose up` chạy OK
- [ ] Container running
- [ ] Xem được log

### CI/CD
- [ ] Có GitHub Actions
- [ ] Pipeline chạy OK
- [ ] Có lint + test + build
- [ ] Không hardcode secret

### Deploy
- [ ] Deploy lại được
- [ ] Không phụ thuộc local

### Environment
- [ ] Có `.env.example`
- [ ] Không commit `.env`

### Debug
- [ ] Demo được incident
- [ ] Xác định đúng layer
- [ ] Fix thành công

## 11. Kết luận
Dự án đã sẵn sàng để demo theo tư duy DevOps: chạy production, deploy lại được, quan sát được log, và debug có hệ thống theo layer.