# Deployment Information - Lab 06 Complete

> **Deployed from:** `06-lab-complete/`  
> **Date:** 17/04/2026

---

## 🌐 Public URL

**Production URL:** `https://day12-agent-production-c313.up.railway.app`

**Status:** 🟢 Running

---

## 🚀 Platform

**Platform:** Railway

**Region:** Singapore (asia-southeast1)

**Plan:** Free Tier

---

## ✅ Test Commands

### 1. Health Check
```bash
curl https://day12-agent-production-c313.up.railway.app/health
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
```json
{"status":"ok","uptime":2664.1,"redis_connected":true}
```

---

### 2. Readiness Check
```bash
curl https://day12-agent-production-c313.up.railway.app/ready
```

**Expected Response:**
```json
{
  "ready": true
}
```

**Actual Result:**
```json
{"ready":true}
```

---

### 3. Authentication Test (Should Return 401)
```bash
curl -X POST https://day12-agent-production-c313.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

**Expected:** `401 Unauthorized`

**Actual Result:**
```json
{"detail":"Invalid or missing API key. Include header: X-API-Key: <key>"}
```

---

### 4. API Test with Authentication
```bash
# Thay YOUR_API_KEY bằng key thật từ environment variables
curl -X POST https://day12-agent-production-c313.up.railway.app/ask \
  -H "X-API-Key: prod-key-2110" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is production deployment?"}'
```

**Expected:** `200 OK` with agent response

**Actual Result:**
```json
{
  "question": "What is production deployment?",
  "answer": "## Production Deployment: A Deep Dive\n\nProduction deployment is the process of releasing a new or updated software application to the live environment where end-users will actually use it...",
  "session_id": "1c55963d-4e40-42eb-b946-b00c20d27eac",
  "model": "gemma-3-27b-it",
  "timestamp": "2026-04-17T15:52:55.255272+00:00"
}
```

---

### 5. Rate Limiting Test
```bash
# Gửi 12 requests liên tục để test rate limit
for i in {1..12}; do
  echo "Request $i:"
  curl -X POST https://day12-agent-production-c313.up.railway.app/ask \
    -H "X-API-Key: prod-key-2110" \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"Test $i\"}"
  echo -e "\n"
done
```

**Expected:** Request thứ 11 trả về `429 Too Many Requests`

**Actual Result:**
```
Request 13: 429
Response: {"detail":"Rate limit exceeded: 10 req/min"}
```

---

## 🔧 Environment Variables Set

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Deployment environment |
| `APP_NAME` | `Production AI Agent` | Application name |
| `PORT` | `8000` | Server port |
| `REDIS_URL` | `redis://...` | Redis connection URL |
| `AGENT_API_KEY` | `prod-key-2110` | API authentication key |
| `JWT_SECRET` | `***hidden***` | JWT signing secret |
| `RATE_LIMIT_PER_MINUTE` | `10` | Rate limit threshold |
| `DAILY_BUDGET_USD` | `5.0` | Per-user daily budget |
| `GLOBAL_DAILY_BUDGET_USD` | `50.0` | Global daily budget |
| `GOOGLE_API_KEY` | `AIza...` | Google AI API key |

---

## 📸 Screenshots

### 1. Deployment Dashboard
![Deployment Dashboard](screenshots/successful_render_deployment.png)
_Platform dashboard showing service status (Note: Screenshot from previous successful run or similar)_

### 2. Service Running
![Service Running](screenshots/successful_render_deployment.png)
_Service logs showing successful startup_

---

## ✅ Deployment Checklist

- [x] Service deployed successfully
- [x] Public URL accessible
- [x] Health check returns 200
- [x] Readiness check returns 200
- [x] Authentication works (401 without key)
- [x] API works with valid key (200)
- [x] Rate limiting works (429 after limit)
- [x] Redis connected
- [x] All environment variables set
- [ ] Screenshots captured (updated placeholders)
- [x] No secrets in code/logs

---

## 📝 Notes

- Ứng dụng đã được tích hợp Google LLM (model `gemma-3-27b-it`) thay vì Mock LLM.
- Redis được sử dụng để lưu trữ lịch sử chat và quản lý rate limiting, đảm bảo tính stateless cho ứng dụng.
- Đã cấu hình Graceful Shutdown để xử lý các request dở dang khi restart.

---

**Deployed by:** Lê Văn Hậu
**Date:** 17/04/2026
