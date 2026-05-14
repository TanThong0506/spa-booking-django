# Spa Booking Django

## Mô tả
Website quản lý đặt lịch dịch vụ Spa/Salon bằng Django.

## Công nghệ sử dụng
- Django
- MySQL/MariaDB bằng XAMPP
- HTML/CSS

## Chức năng đã làm
- Đăng ký / đăng nhập
- Xem danh sách dịch vụ
- Đặt lịch
- Xem lịch hẹn cá nhân
- Hủy lịch
- Dashboard thống kê
- Phân quyền admin
## Tình trạng dự án
- **CI/CD:** Đã tích hợp GitHub Actions (Lint, Test, Build) thành công.
## Cách chạy project
```bash
python -m venv venv
venv\Scripts\activate
pip install django pymysql pillow
python manage.py migrate
python manage.py runserver
```

## Production (an toàn/ổn định)

### 1. Chuẩn bị biến môi trường
1. Tạo file `.env.production` từ `.env.example`.
2. Bắt buộc đổi các giá trị:
- `SECRET_KEY`
- `DB_PASSWORD`
- `DB_ROOT_PASSWORD`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

### 2. Chạy stack production với Docker Compose
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### 3. Kiểm tra container
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f nginx
```

### 4. Dừng hệ thống
```bash
docker compose -f docker-compose.prod.yml down
```

## Thành phần production
- `web`: Django + Gunicorn
- `db`: MySQL 8
- `nginx`: reverse proxy, static/media serving

## Ghi chú bảo mật
- Không dùng `ALLOWED_HOSTS=*` trên môi trường production.
- Luôn chạy HTTPS ở lớp ngoài (Cloudflare/Nginx TLS).
- Không commit file `.env` chứa mật khẩu thật.