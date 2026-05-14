# Deploy lên Render.com (Free tier)

## Tại sao Render?
- Free tier có thể host 1 web service
- Tự động build từ GitHub
- Auto-deploy khi push
- Database PostgreSQL free (5GB storage)
- Custom domain support
- HTTPS tự động

## Step 1: Tạo Render account
1. Vào https://render.com
2. Click **Sign up** → chọn **Sign up with GitHub**
3. Authorize Render truy cập repo

## Step 2: Create Web Service
1. Vào Dashboard → Click **New +** → **Web Service**
2. **Connect a repository:**
   - Tìm `spa-booking-django`
   - Click **Connect**

3. **Configure:**
   - **Name:** `spa-booking` (auto-generate)
   - **Environment:** Docker
   - **Build Command:** `./render-build.sh`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT spa_booking.wsgi:application`
   - **Instance Type:** Free

4. **Add Environment Variables:**
   Click **Advanced** → **Add Environment Variable**
   
   Thêm từng cái:
   ```
   SECRET_KEY = (generate long random string)
   DEBUG = False
   ENVIRONMENT = production
   DB_ENGINE = postgresql
   DB_NAME = (Render tự tạo)
   DB_USER = (Render tự tạo)
   DB_PASSWORD = (Render tự tạo)
   DB_HOST = (Render tự tạo)
   ALLOWED_HOSTS = your-render-app.onrender.com
   CSRF_TRUSTED_ORIGINS = https://your-render-app.onrender.com
   CORS_ALLOWED_ORIGINS = https://your-render-app.onrender.com
   ```

5. Click **Deploy** → chờ build hoàn tất (~5-10 phút)

## Step 3: Lấy URL
Sau khi deploy thành công:
- Render sẽ cấp URL: `https://spa-booking-xxx.onrender.com`
- Click link → app chạy ngay!

## Step 4: Auto-deploy từ GitHub (tùy chọn)
- Render đã config **autoDeploy: true**
- Mỗi lần push `main` → Render tự build + deploy

## Troubleshooting
- **Build fail:** Check buildlog trong Render dashboard
- **App crash:** Click **Logs** để xem error
- **Database sai:** Verify env vars trên Render

## Notes
- Free tier: "spins down" sau 15min không dùng (đầu start chậm)
- Upgrade nếu muốn production: **Standard Plan** ($7/tháng)
- Backup database: Render cung cấp automatic backup
