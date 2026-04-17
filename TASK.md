# TASK - Lab Ngày 12 (17/04/2026)

## Tổng quan
- Mục tiêu: Đưa AI agent từ localhost lên production và cloud theo chuẩn triển khai thực tế.
- Phạm vi: Hoàn thành chuỗi bài 01 → 06 trong lab Ngày 12.

## Tổng hợp công việc hôm nay

### Phần 1 - Localhost vs Production
- Rà soát anti-pattern trong bản develop (hardcode secret, port cố định, debug mode, thiếu health check).
- So sánh bản develop và production theo nguyên tắc 12-Factor.
- Chuẩn hóa cấu hình qua environment variables.

### Phần 2 - Docker
- Đọc và phân tích Dockerfile cơ bản.
- Build và chạy image develop để xác minh app chạy trong container.
- Phân tích Dockerfile production với multi-stage build.
- Chạy stack với docker compose và test endpoint health/ask.

### Phần 3 - Cloud Deployment
- Chọn nền tảng deploy (Railway/Render/Cloud Run).
- Chuẩn bị biến môi trường và cấu hình deploy.
- Triển khai bản app public và xác minh URL truy cập được.

### Phần 4 - API Gateway & Security
- Thiết lập cơ chế xác thực API key/JWT.
- Bổ sung rate limiting (mục tiêu 10 req/phút).
- Thêm cost guard (giới hạn ngân sách tháng).
- Kiểm thử các mã lỗi 401/429/402 theo tình huống.

### Phần 5 - Scaling & Reliability
- Thêm health check/readiness check.
- Cấu hình graceful shutdown.
- Triển khai stateless design, tách state sang Redis.
- Kiểm thử hành vi khi scale nhiều instance.

### Phần 6 - Lab Complete (Production Ready)
- Hợp nhất các thành phần vào bộ mã hoàn chỉnh trong thư mục 06-lab-complete.
- Đóng gói Dockerfile production và docker-compose full stack.
- Kiểm tra không hardcode secret, sử dụng env variables.
- Rà soát README hướng dẫn chạy và deploy.

## Tài liệu/kết quả cần nộp
- MISSION_ANSWERS.md: trả lời toàn bộ bài tập theo từng Phần.
- DEPLOYMENT.md: URL public, lệnh test, platform, biến môi trường, screenshot.
- Source code final day 12 (production-ready) theo cấu trúc yêu cầu.

## Tiêu chí xác minh trước khi nộp
- App chạy ổn định, không lỗi runtime cơ bản.
- Có authentication, rate limiting, cost guard.
- Có health endpoint và readiness endpoint.
- Hỗ trợ stateless + Redis khi scale.
- Docker image production đạt mục tiêu gọn nhẹ.
- Không commit secret, không đẩy file .env thật.

## Kế hoạch tiếp theo
- Hoàn tất screenshot dashboard + kết quả test.
- Điền đầy đủ MISSION_ANSWERS.md và DEPLOYMENT.md.
- Chạy self-test lần cuối trước khi nộp repo.
