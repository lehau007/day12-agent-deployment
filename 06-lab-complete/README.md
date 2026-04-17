# 🚀 Production AI Agent — Lab 12 Complete

Đây là phiên bản hoàn chỉnh của AI Agent được xây dựng trong Lab 12, tích hợp đầy đủ các tiêu chuẩn Production-ready: Docker, Security, Rate Limiting, Cost Guard, và Stateless Session.

**🔗 Live Demo:** [https://day12-agent-production-781b.up.railway.app](https://day12-agent-production-781b.up.railway.app)

---

## ✨ Tính Năng Nổi Bật

- **🤖 Real AI Chat:** Đã tích hợp **Google Gemini API** (thư viện `google-genai`). Agent có khả năng ghi nhớ ngữ cảnh hội thoại thông qua `session_id`.
- **🔐 Bảo mật:** Xác thực qua `X-API-Key` header cho mọi request.
- **🛡️ Rate Limiting:** Giới hạn 10 requests/phút cho mỗi người dùng để tránh lạm dụng.
- **💰 Cost Guard:** Tự động theo dõi chi phí và chặn request nếu vượt quá ngân sách hàng ngày (mặc định $10/user).
- **📦 Dockerized:** Multi-stage build tối ưu kích thước (< 200MB), chạy với Non-root user để bảo mật tối đa.
- **📡 Stateless:** Lưu trữ lịch sử chat trong Redis (nếu có) hoặc bộ nhớ tạm, giúp scale ngang dễ dàng.
- **🏥 Health & Readiness:** Cung cấp endpoint `/health` và `/ready` cho các hệ thống giám sát và cân bằng tải.

---

## 💻 Cách Chạy Local

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt Python 3.10+ và đã cài các thư viện cần thiết:

```bash
cd 06-lab-complete
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường
Tạo file `.env` từ mẫu có sẵn:

```bash
cp .env.example .env
```

Mở file `.env` và cập nhật các thông tin quan trọng:
- **`GOOGLE_API_KEY`**: API Key từ Google AI Studio (Gemini).
- `AGENT_API_KEY`: Key dùng để gọi API (ví dụ: `my-secret-key`).
- `REDIS_URL`: Để trống nếu không dùng Redis (mặc định sẽ dùng bộ nhớ trong).

### 3. Chạy ứng dụng

**Cách 1: Chạy trực tiếp với Python**
```bash
$env:PYTHONPATH="."; uvicorn app.main:app --reload
```

**Cách 2: Chạy với Docker Compose (Khuyên dùng)**
```bash
docker-compose up --build
```

---

## 🧪 Kiểm tra API

Sau khi server khởi động (mặc định tại `http://localhost:8000`), bạn có thể test bằng `curl` hoặc Postman:

**1. Kiểm tra trạng thái:**
```bash
curl http://localhost:8000/health
```

**2. Gửi câu hỏi (Chat):**
```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-agent-api-key-here" \
     -d '{"question": "Xin chào, bạn là ai?", "session_id": "user-123"}'
```

---

## 🚢 Deploy lên Railway

Dự án này đã được cấu hình sẵn cho Railway thông qua file `railway.toml`.
1. Kết nối repo này với Railway.
2. Thêm các Variables: **`GOOGLE_API_KEY`**, `AGENT_API_KEY`.
3. Railway sẽ tự động build và deploy từ `Dockerfile`.

---
*Dự án thuộc nội dung Lab 12 — VinUni.*
