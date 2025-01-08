# เริ่มต้นจาก Python official image
FROM python:3.9-slim

# ติดตั้ง dependencies ที่จำเป็น
RUN pip install --no-cache-dir --upgrade pip

# สร้าง directory สำหรับทำงาน
RUN mkdir /sandbox
WORKDIR /sandbox

# ตั้งค่าการจำกัด resources
# นี่จะถูกกำหนดในขณะรัน Docker container โดยใช้ option `--memory` และ `--cpus`

# คำสั่งที่จะรันโค้ด
# CMD ["python", "user_code.py"]
