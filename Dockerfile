# Python 3.12 베이스 이미지
FROM python:3.12-slim

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# 비root 사용자 생성
RUN groupadd -r django && useradd -r -g django -m django

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (PostgreSQL 클라이언트 등)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN pip install uv

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen

# 프로젝트 파일 복사
COPY . .

# 정적 파일 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app

# django 유저로 전환
USER django

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD uv run curl -f http://localhost:8000/admin/ || exit 1

# 개발 서버 실행
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]