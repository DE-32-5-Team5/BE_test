# Python 이미지를 베이스로 사용
FROM python:3.9-slim

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 파일 복사
COPY ./app.py /app/app.py

# Uvicorn을 통해 FastAPI 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

