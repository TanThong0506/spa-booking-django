#!/usr/bin/env bash
# Exit on error
set -o errexit

# Cài đặt thư viện
pip install -r requirements.txt

# Xử lý file tĩnh giao diện
python manage.py collectstatic --no-input

# Tự động tạo và áp dụng cập nhật Database (Fix lỗi thiếu thư mục apppointment lúc nãy)
python manage.py makemigrations
python manage.py migrate