# 🚂 Deploy lên Railway - Đơn Giản Nhất!

## ✅ Tại sao chọn Railway?

- ✅ **Redis FREE** (không như Render)
- ✅ Deploy trong **5 phút**
- ✅ CLI đơn giản
- ✅ Auto-detect Dockerfile
- ✅ $5 credit miễn phí

---

## 📋 BƯỚC 1: Cài Railway CLI (1 phút)

```bash
# Windows (PowerShell)
npm install -g @railway/cli

# Hoặc dùng Scoop
scoop install railway
```

Verify:
```bash
railway --version
```

---

## 📋 BƯỚC 2: Login (30 giây)

```bash
railway login
```

Trình duyệt sẽ mở → Đăng nhập bằng GitHub

---

## 📋 BƯỚC 3: Init Project (1 phút)

```bash
cd 06-lab-complete
railway init
```

Chọn:
- **Create a new project**
- Đặt tên: `day12-production-agent`

---

## 📋 BƯỚC 4: Thêm Redis (30 giây)

```bash
railway add
```

Chọn: **Redis** (dùng mũi tên ↑↓ và Enter)
Lên Railway tìm service Redis tìm biến `REDIS_URL` (dạng: `redis://...`) và copy lại để test kết nối sau này.

railway add 
Chọn empty
---

## 📋 BƯỚC 5: Set Environment Variables (1 phút)

```bash
railway variables set ENVIRONMENT=production
railway variables set REDIS_URL=redis://...
railway variables set APP_NAME="Production AI Agent"
railway variables set GOOGLE_API_KEY=AIza...
railway variables set LLM_MODEL=gemma-3-27b-it
railway variables set AGENT_API_KEY=prod-key-2110
railway variables set JWT_SECRET=jwt-secret-2110
railway variables set RATE_LIMIT_PER_MINUTE=10
railway variables set DAILY_BUDGET_USD=5.0
railway variables set GLOBAL_DAILY_BUDGET_USD=50.0
```
 
**Xem tất cả variables:**
```bash
railway variables
```

---

## 📋 BƯỚC 6: Deploy! (2 phút)

```bash
railway up
```

Railway sẽ:
1. Detect Dockerfile
2. Build image (~1-2 phút)
3. Deploy container
4. Start app

Xem logs:
```bash
railway logs
```

Tìm dòng:
```
✅ Connected to Redis
✅ Application startup complete
```

---

## 📋 BƯỚC 7: Lấy Public URL (30 giây)

```bash
railway domain
```

Nếu chưa có domain, tạo mới:
```bash
railway domain create
```

Copy URL (dạng: `https://day12-production-agent-production.up.railway.app`)

---

## ✅ BƯỚC 8: Test Deployment

### Quick Test
```bash
# Thay YOUR_URL
curl https://YOUR_URL/health
```

Expected:
```json
{
  "status": "ok",
  "uptime": 123.4,
  "redis_connected": true
}
```

### Full Test
```bash
# Lấy API key
railway variables | grep AGENT_API_KEY

# Test với script
cd 06-lab-complete
.\test_deployment.ps1 -Url "https://YOUR_URL" -ApiKey "YOUR_KEY"
```

---

## 📸 Screenshots

Chụp:
1. **Terminal** - Output của `railway up`
2. **Dashboard** - https://railway.app/dashboard
3. **Logs** - Output của `railway logs`
4. **Test Results** - Output của test script

---

## 🎯 Useful Commands

```bash
# Xem status
railway status

# Xem logs real-time
railway logs --follow

# Xem variables
railway variables

# Set variable mới
railway variables set KEY=value

# Xóa variable
railway variables delete KEY

# Restart service
railway restart

# Open dashboard
railway open
```

---

## 🐛 Troubleshooting

### "No project found"
```bash
railway link
# Chọn project từ list
```

### "Build failed"
```bash
railway logs
# Xem lỗi cụ thể
```

### "Redis connection failed"
```bash
railway variables | grep REDIS_URL
# Kiểm tra REDIS_URL có tồn tại không
```

### "Out of credits"
- Free tier: $5/month
- Xem usage: https://railway.app/account/usage
- Upgrade nếu cần

---

## 💰 Pricing

**Free Tier:**
- $5 credit/month
- Đủ cho lab này (~$2-3/month)
- Không cần credit card

**Usage:**
- Web service: ~$1-2/month
- Redis: ~$0.5/month
- Total: ~$2-3/month

---

## 🎉 DONE!

Sau khi deploy xong:

1. Copy URL vào `DEPLOYMENT.md`
2. Chạy test script
3. Paste kết quả vào `DEPLOYMENT.md`
4. Chụp screenshots
5. Commit và push

**Thời gian tổng: ~5 phút**

**Railway > Render** vì có Redis free! 🚀
