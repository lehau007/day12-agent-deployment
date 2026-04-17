 1. Phần chuẩn bị & Học tập (Research & Learning)
   * Đọc kỹ CODE_LAB.md: Đây là tài liệu quan trọng nhất hướng dẫn từng bước từ Phần 1 đến Phần 6.
   * Phân tích các Anti-patterns: Xem mã nguồn trong 01-localhost-vs-production/develop để tìm các lỗi như hardcode secret, port cố định, thiếu health
     check.

  2. Phần thực hành & Trả lời câu hỏi (Exercises)
  Bạn cần thực hiện các bài tập trong từng thư mục và ghi lại câu trả lời vào file MISSION_ANSWERS.md:
   * Phần 1: So sánh Dev vs Production, chuẩn hóa biến môi trường.
   * Phần 2: Build Docker image. So sánh kích thước Image giữa bản develop và bản production (multi-stage build).
   * Phần 3: Deploy app lên Cloud (Railway/Render) và lấy URL public.
   * Phần 4: Cấu hình bảo mật (Auth, Rate Limiting 10 req/phút, Cost Guard $10/tháng).
   * Phần 5: Cấu hình Health check, Readiness check, Graceful shutdown và Stateless (dùng Redis).

  3. Phần hoàn thiện Code (Final Project - Lab 06)
  Hợp nhất tất cả vào thư mục 06-lab-complete (hoặc cấu trúc repo nộp bài) với các yêu cầu kỹ thuật:
   * [ ] Mã nguồn nằm trong thư mục app/.
   * [ ] Dockerfile phải là multi-stage build (kích thước < 500MB).
   * [ ] Có file docker-compose.yml chạy được cả stack (App + Redis).
   * [ ] File .env.example đầy đủ các biến cần thiết (AGENT_API_KEY, REDIS_URL, PORT...).
   * [ ] TUYỆT ĐỐI KHÔNG commit file .env thật hoặc hardcode API Key.

  4. Phần triển khai & Minh chứng (Deployment & Evidence)
  Tạo file DEPLOYMENT.md bao gồm:
   * [ ] URL public của ứng dụng đang chạy.
   * [ ] Các lệnh curl để test: Health check, API Auth, và Rate Limiting.
   * [ ] Danh sách các biến môi trường đã set trên Cloud.
   * [ ] Screenshots: Chụp ảnh Dashboard Cloud, ứng dụng đang chạy, và kết quả test. Lưu vào thư mục screenshots/.

  5. Kiểm tra cuối cùng (Self-Test) trước khi nộp
   * [ ] Kiểm tra URL public có truy cập được từ thiết bị khác không.
   * [ ] Chạy thử lệnh test Rate Limiting (gửi > 10 request) xem có trả về lỗi 429 không.
   * [ ] Kiểm tra xem đã trả lời hết các câu hỏi trong MISSION_ANSWERS.md chưa.
   * [ ] Đảm bảo Repo GitHub ở chế độ Public hoặc giảng viên có quyền truy cập.

  Lời khuyên: Bạn nên làm tuần tự từ Phần 1 đến Phần 5 để tích lũy dần các tính năng cho Phần 6. Phần 6 chính là bản tổng hợp của tất cả các phần trước.