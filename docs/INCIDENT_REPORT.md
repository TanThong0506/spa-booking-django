# INCIDENT REPORT (QA/SRE)

## Incident 1 — API trả 500 tại `/api/health`
- **Hiện tượng:** gọi health endpoint trả 500, body báo `database: disconnected`
- **Layer lỗi:** L3 Backend (liên quan L2 DB)
- **Nguyên nhân:** cấu hình DB sai (`DB_HOST`/`DB_PORT`/`DB_PASSWORD`) hoặc DB chưa sẵn sàng
- **Cách fix:**
  1. Kiểm tra env DB
  2. Kiểm tra trạng thái container db (`docker compose ps`)
  3. Dùng healthcheck và `depends_on.condition: service_healthy`
- **Phòng tránh:**
  - Không hardcode DB config
  - Có healthcheck DB trong compose
  - Có endpoint health cho monitoring

---

## Incident 2 — CORS lỗi khi FE gọi API
- **Hiện tượng:** browser báo `CORS policy blocked`
- **Layer lỗi:** L4 Frontend / L3 Backend config
- **Nguyên nhân:** thiếu domain frontend trong `CORS_ALLOWED_ORIGINS`
- **Cách fix:**
  1. Bổ sung domain frontend vào env `CORS_ALLOWED_ORIGINS`
  2. Reload/redeploy backend
- **Phòng tránh:**
  - Tách config theo môi trường
  - Không hardcode origin trong code
  - Dùng checklist deploy bắt buộc có bước kiểm tra CORS

---

## Incident 3 — Deploy thành công nhưng truy cập lỗi 400 Bad Request
- **Hiện tượng:** Nginx trả 400, app không vào được
- **Layer lỗi:** L1 Infrastructure / L3 Backend
- **Nguyên nhân:** `ALLOWED_HOSTS` và `CSRF_TRUSTED_ORIGINS` thiếu domain thực tế
- **Cách fix:**
  1. Cập nhật `.env.production`
  2. Set đúng `ALLOWED_HOSTS` (domain, www)
  3. Set đúng `CSRF_TRUSTED_ORIGINS` (https://domain)
  4. Redeploy containers
- **Phòng tránh:**
  - Dùng `.env.production.example` làm template chuẩn
  - Verify env trước deploy bằng checklist

---

## Lệnh điều tra chuẩn khi incident
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f db
docker compose -f docker-compose.prod.yml logs -f nginx
```

```bash
curl http://127.0.0.1:18080/api/health
```

## Kết luận
Ba incident trên bao phủ các lớp lỗi phổ biến (L1/L2/L3/L4) và phù hợp yêu cầu môn học về system thinking trong debug.