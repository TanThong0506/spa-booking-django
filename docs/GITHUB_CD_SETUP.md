# GitHub Actions CD Setup Guide

## Tổng quan
CD workflow (`.github/workflows/cd_deploy.yml`) hỗ trợ 2 cách deploy thực tế:
- **Render.com** (easiest, free tier)
- **VPS SSH** (full control)

## Option 1: Deploy lên Render

### 1.1 Tạo app trên Render
1. Vào https://render.com
2. Tạo **New Web Service** từ GitHub repo
3. Config:
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start command: `gunicorn --bind 0.0.0.0:8000 spa_booking.wsgi:application`
   - Add env vars (xem `.env.production.example`)

### 1.2 Tạo Deploy Hook
1. Vào Render dashboard → Settings
2. Copy **Deploy Hook URL** (dạng `https://api.render.com/deploy/srv-...`)

### 1.3 Config GitHub Secrets
1. Vào repo GitHub → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Thêm:
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: (paste URL từ Render)

### 1.4 Config GitHub Variables
1. Vào repo GitHub → **Settings → Secrets and variables → Actions → Variables**
2. Click **New repository variable**
3. Thêm:
   - Name: `PRODUCTION_RENDER_URL`
   - Value: `https://your-render-app.onrender.com`

### 1.5 Test
Push commit mới vào `main` → workflow chạy → xem tab **Deployments**

---

## Option 2: Deploy lên VPS via SSH

### 2.1 Chuẩn bị VPS
1. SSH vào VPS
2. Clone repo vào folder (ví dụ: `/home/ubuntu/spa-booking`)
   ```bash
   git clone <repo-url>
   cd spa-booking
   cp .env.production.example .env.production
   # Edit .env.production với giá trị thật
   docker compose -f docker-compose.prod.yml up -d
   ```

### 2.2 Tạo SSH key cho deploy
Trên VPS:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""
cat ~/.ssh/github_deploy.pub >> ~/.ssh/authorized_keys
```

Trên local (để copy về):
```bash
cat ~/.ssh/github_deploy
```

### 2.3 Config GitHub Secrets
1. Vào repo GitHub → **Settings → Secrets and variables → Actions**
2. Click **New repository secret** và thêm:

| Name | Value |
|------|-------|
| `VPS_HOST` | `your-vps-ip-or-domain` |
| `VPS_USER` | `ubuntu` (hoặc user trên VPS) |
| `VPS_SSH_KEY` | (paste private key `github_deploy` từ VPS) |
| `VPS_APP_PATH` | `/home/ubuntu/spa-booking` |

### 2.4 Config GitHub Variables
1. Vào **Settings → Secrets and variables → Actions → Variables**
2. Thêm:
   - Name: `PRODUCTION_VPS_URL`
   - Value: `http://your-vps-ip:18080` (hoặc domain)

### 2.5 Test
Push commit mới → workflow chạy → kiểm tra VPS

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
```

---

## Lưu ý bảo mật

⚠️ **SSH Key Security:**
- Không commit private key
- Rotate key định kỳ
- GitHub hỗ trợ mask secret trong log

⚠️ **Env Variables:**
- Không hardcode password trong code
- Sử dụng `.env.production` với `git-crypt` hoặc chỉ store locally

⚠️ **CORS & ALLOWED_HOSTS:**
- Update `.env.production` với domain thực tế
- Redeploy sau khi update env

---

## Troubleshooting

### Deployment không chạy
- Kiểm tra Secrets và Variables đã config đúng chưa
- Xem **Actions tab** → run log

### Render deploy fail
- Kiểm tra env vars trên Render dashboard
- Xem Render build log

### VPS deploy fail
- Kiểm tra SSH key permissions: `chmod 600 ~/.ssh/authorized_keys`
- Test SSH: `ssh -i ~/.ssh/github_deploy ubuntu@your-vps-ip`
- Kiểm tra git pull quyền: `git pull origin main` phải chạy được trong VPS

---

## GitHub Deployments Tab

Sau khi deploy thành công, bạn sẽ thấy:
- **Deployments** tab hiển thị lịch sử
- Environment: `Production (Render)` hoặc `Production (VPS)`
- Click để xem deployment details