# Day 12 — Deployment: Đưa Agent Lên Cloud

> **AICB-P1 · VinUniversity 2026**  
> Repository thực hành đi kèm bài giảng Day 12.

---

## 🌐 PRODUCTION DEPLOYMENT

**Link truy cập web:** [https://day12-agent-production-c313.up.railway.app](https://day12-agent-production-c313.up.railway.app)

**Trạng thái:** 🟢 Hoạt động (Railway)  
**Tính năng nổi bật:**
- 🤖 **Google LLM Integration:** Đã tích hợp mô hình `gemma-3-27b-it` của Google thay vì sử dụng Mock LLM.
- 🔐 **Security:** API Key Authentication (`X-API-Key`).
- ⚡ **Performance:** Redis-backed rate limiting & chat history.
- 🛡️ **Reliability:** Health checks & Graceful shutdown.

---

## Cấu Trúc Project

```
day12_ha-tang-cloud_va_deployment/
├── 01-localhost-vs-production/     # Section 1: Dev ≠ Production
├── 02-docker/                      # Section 2: Containerization
├── 03-cloud-deployment/            # Section 3: Cloud Options
├── 04-api-gateway/                 # Section 4: Security
├── 05-scaling-reliability/         # Section 5: Scale & Reliability
├── 06-lab-complete/                # Lab 12: Production-ready agent (DỰ ÁN CHÍNH)
└── utils/                          # Mock LLM dùng chung
```

---

## 🛠️ Chạy Local (06-lab-complete)
---

## 🛠️ Chạy Local (06-lab-complete) với Docker Compose

Để chạy phiên bản hoàn chỉnh nhất (`06-lab-complete`) trên máy tính cá nhân bằng Docker:

### 1. Chuẩn bị cấu hình
Di chuyển vào thư mục dự án và tạo file `.env.local` (được sử dụng bởi docker-compose):
```bash
cd 06-lab-complete
cp .env.example .env.local
```
Cập nhật `GOOGLE_API_KEY` trong file `.env.local` với API key từ Google AI Studio của bạn.

### 2. Khởi chạy với Docker Compose
```bash
docker-compose up --build
```
Lệnh này sẽ tự động:
- Build image cho AI Agent từ Dockerfile.
- Khởi tạo một container Redis riêng biệt.
- Kết nối Agent với Redis để lưu trữ lịch sử chat và quản lý rate limit.

### 3. Kiểm tra
- Health check: `curl http://localhost:8000/health`
- Thử nghiệm chat:
```bash
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: dev-key-change-me" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Hello!\"}"
```

---

## 🚀 Các Phần Khác

**Muốn học kỹ?** → [CODE_LAB.md](CODE_LAB.md) (3-4 giờ)

| Bước | Làm gì |
|------|--------|
| 1 | Đọc [CODE_LAB.md](CODE_LAB.md) để hiểu chi tiết |
| 2 | Chạy ví dụ **basic** trước — hiểu concept |
| 3 | So sánh với ví dụ **advanced** — thấy sự khác biệt |
| 4 | Tự làm Lab 06 từ đầu trước khi xem solution |

---

## Yêu Cầu Hệ Thống

```bash
python 3.11+
docker & docker compose
```

---

## 📊 Lab Materials

| Tài liệu | Mô tả |
|----------|-------|
| **[CODE_LAB.md](CODE_LAB.md)** | Hướng dẫn lab chi tiết từng bước |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Thông tin chi tiết về bản deploy Production |
| **[MISSION_ANSWERS.md](MISSION_ANSWERS.md)** | Câu trả lời cho các bài tập lý thuyết |

**Deployed by:** Lê Văn Hậu
