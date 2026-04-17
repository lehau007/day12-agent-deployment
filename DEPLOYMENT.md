# Deployment Information

## Public URL
https://your-agent.railway.app (Thay bằng URL thật của bạn)

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok", "redis_connected": true}
```

### API Test (with authentication)
```bash
# 1. Login để lấy token
curl -X POST https://your-agent.railway.app/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "password": "demo123"}'

# 2. Sử dụng token để hỏi Agent
curl -X POST https://your-agent.railway.app/ask \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"question": "How to deploy an AI agent?"}'
```

## Environment Variables Set
- `PORT`: 8000
- `REDIS_URL`: redis://...
- `JWT_SECRET`: <your-secret>
- `ENVIRONMENT`: production
- `AGENT_API_KEY`: <your-key>

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
