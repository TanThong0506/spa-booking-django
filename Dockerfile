# Sử dụng Python bản ổn định
FROM python:3.10-slim

# Cài đặt các công cụ cần thiết cho MySQL và build
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy lệnh thu thập tệp tĩnh (để đạt điểm phần Build)
RUN python manage.py collectstatic --noinput

# Chạy ứng dụng bằng Gunicorn (chuẩn Production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "spa_booking.wsgi:application"]