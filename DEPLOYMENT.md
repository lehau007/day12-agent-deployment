# Deployment Information - Lab 06 Complete

> **Deployed from:** `06-lab-complete/`  
> **Date:** 17/04/2026

---

## 🌐 Public URL

**Production URL:** `https://YOUR_ACTUAL_URL_HERE`

**Status:** 🟢 Running | 🔴 Down | 🟡 Deploying

---

## 🚀 Platform

**Platform:** Railway / Render _(chọn một)_

**Region:** Singapore / US East _(chọn một)_

**Plan:** Free Tier / Starter

---

## ✅ Test Commands

### 1. Health Check
```bash
curl https://YOUR_ACTUAL_URL_HERE/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "uptime": 123.4,
  "redis_connected": true
}
```

**Actual Result:**
```
[Paste kết quả test ở đây]
```

---

### 2. Readiness Check
```bash
curl https://YOUR_ACTUAL_URL_HERE/ready
```

**Expected Response:**
```json
{
  "ready": true
}
```

**Actual Result:**
```
[Paste kết quả test ở đây]
```

---

### 3. Authentication Test (Should Return 401)
```bash
curl -X POST https://YOUR_ACTUAL_URL_HERE/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

**Expected:** `401 Unauthorized`

**Actual Result:**
```
[Paste kết quả test ở đây]
```

---

### 4. API Test with Authentication
```bash
# Thay YOUR_API_KEY bằng key thật từ environment variables
curl -X POST https://YOUR_ACTUAL_URL_HERE/ask \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is production deployment?"}'
```

**Expected:** `200 OK` with agent response

**Actual Result:**
```json
[Paste kết quả test ở đây]
```

---

### 5. Rate Limiting Test
```bash
# Gửi 12 requests liên tục để test rate limit
for i in {1..12}; do
  echo "Request $i:"
  curl -X POST https://YOUR_ACTUAL_URL_HERE/ask \
    -H "X-API-Key: YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"Test $i\"}"
  echo -e "\n"
done
```

**Expected:** Request thứ 11 trả về `429 Too Many Requests`

**Actual Result:**
```
[Paste kết quả test ở đây - chỉ cần request cuối cùng bị rate limit]
```

---

## 🔧 Environment Variables Set

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Deployment environment |
| `APP_NAME` | `Production AI Agent` | Application name |
| `PORT` | `8000` | Server port |
| `REDIS_URL` | `redis://...` | Redis connection URL |
| `AGENT_API_KEY` | `***hidden***` | API authentication key |
| `JWT_SECRET` | `***hidden***` | JWT signing secret |
| `RATE_LIMIT_PER_MINUTE` | `10` | Rate limit threshold |
| `DAILY_BUDGET_USD` | `5.0` | Per-user daily budget |
| `GLOBAL_DAILY_BUDGET_USD` | `50.0` | Global daily budget |
| `OPENAI_API_KEY` | _(empty - using mock)_ | OpenAI API key |

---

## 📸 Screenshots

### 1. Deployment Dashboard
![Deployment Dashboard](screenshots/06-dashboard.png)
_Platform dashboard showing service status_

### 2. Service Running
![Service Running](screenshots/06-running.png)
_Service logs showing successful startup_

### 3. Test Results
![Test Results](screenshots/06-test-results.png)
_Terminal showing successful API calls_

### 4. Rate Limiting in Action
![Rate Limiting](screenshots/06-rate-limit.png)
_429 error when exceeding rate limit_

---

## 📊 Deployment Metrics

**Build Time:** ~X minutes

**Image Size:** ~236 MB (multi-stage optimized)

**Startup Time:** ~X seconds

**Memory Usage:** ~XXX MB

**CPU Usage:** ~X%

---

## 🔗 Useful Links

- **Service Dashboard:** [Link to platform dashboard]
- **Logs:** [Link to logs page]
- **Metrics:** [Link to metrics page]
- **GitHub Repo:** [Your repo URL]

---

## ✅ Deployment Checklist

- [ ] Service deployed successfully
- [ ] Public URL accessible
- [ ] Health check returns 200
- [ ] Readiness check returns 200
- [ ] Authentication works (401 without key)
- [ ] API works with valid key (200)
- [ ] Rate limiting works (429 after limit)
- [ ] Redis connected
- [ ] All environment variables set
- [ ] Screenshots captured
- [ ] No secrets in code/logs

---

## 📝 Notes

_Ghi chú thêm về deployment, issues gặp phải, hoặc optimizations đã làm_

---

**Deployed by:** [Your Name]  
**Student ID:** [Your ID]  
**Last Updated:** 17/04/2026
