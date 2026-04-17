# ⚡ Quick Deploy Guide - 5 Minutes

## 🚂 Railway (Khuyến nghị - Nhanh nhất)

### 1. Install & Login (1 phút)
```bash
npm install -g @railway/cli
railway login
```

### 2. Deploy (2 phút)
```bash
cd 06-lab-complete
railway init
# Chọn: Create new project → Đặt tên: day12-agent

railway add
# Chọn: Redis

railway up
```

### 3. Set Variables (1 phút)
```bash
railway variables set ENVIRONMENT=production
railway variables set AGENT_API_KEY=secret-$(date +%s)
railway variables set JWT_SECRET=jwt-$(date +%s)
```

### 4. Get URL (30 giây)
```bash
railway domain
# Copy URL này!
```

### 5. Test (30 giây)
```bash
# Thay YOUR_URL
curl https://YOUR_URL/health

# Lấy API key
railway variables | grep AGENT_API_KEY

# Test với key
curl -H "X-API-Key: YOUR_KEY" -X POST https://YOUR_URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

---

## 🎨 Render (Alternative)

### 1. Push to GitHub (1 phút)
```bash
cd 06-lab-complete
git init
git add .
git commit -m "Production agent"
git remote add origin https://github.com/YOUR_USERNAME/day12-agent.git
git push -u origin main
```

### 2. Create Redis (1 phút)
- Vào https://dashboard.render.com
- New → Redis → Free plan
- Copy **Internal Redis URL**

### 3. Create Web Service (2 phút)
- New → Web Service
- Connect GitHub repo
- Root Directory: `06-lab-complete`
- Environment: Docker
- Region: Singapore

### 4. Set Variables (1 phút)
```
ENVIRONMENT=production
REDIS_URL=<paste Redis URL>
AGENT_API_KEY=<random string>
JWT_SECRET=<random string>
```

### 5. Deploy & Test (1 phút)
- Click Deploy
- Đợi build xong
- Copy URL
- Test như Railway

---

## ✅ Quick Test

```bash
# Thay YOUR_URL và YOUR_KEY
URL="https://YOUR_URL"
KEY="YOUR_KEY"

# Health
curl $URL/health

# API
curl -H "X-API-Key: $KEY" -X POST $URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Test deployment"}'
```

---

## 📝 Next Steps

1. Copy URL vào `DEPLOYMENT.md`
2. Chạy full test: `.\test_deployment.ps1 -Url $URL -ApiKey $KEY`
3. Chụp screenshots
4. Update DEPLOYMENT.md với kết quả
5. Done! 🎉
