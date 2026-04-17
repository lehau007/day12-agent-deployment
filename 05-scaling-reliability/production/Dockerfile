FROM python:3.11-slim

WORKDIR /app

# Cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY app.py .
COPY utils/ utils/

EXPOSE 8000

# Lệnh khởi chạy (Dùng uvicorn chuỗi "app:app")
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
