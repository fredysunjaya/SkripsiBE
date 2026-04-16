# ---------------------------
# Stage 1: Builder
# ---------------------------
FROM python:3.11-slim AS builder

WORKDIR /install

# Only build dependencies (removed later)
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# ---------------------------
# Stage 2: Final image
# ---------------------------
FROM python:3.11-slim

WORKDIR /app

# Only runtime libraries (no -dev packages)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN python -c "from deepface import DeepFace; DeepFace.build_model('Facenet')"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy project AFTER deps (better caching)
COPY . .

EXPOSE 8080

CMD ["gunicorn", "skripsiBE.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8080"]