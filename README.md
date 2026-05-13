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