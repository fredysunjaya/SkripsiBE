# ─────────────────────────────────────────────
# Stage 1: Builder
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

# System deps required to compile Python packages and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install/pkg --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────
# Stage 2: Runtime
# ─────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Runtime system libraries (OpenCV / DeepFace dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libgomp1 \
    libhdf5-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install/pkg /usr/local

WORKDIR /app

# Copy project source
COPY . .

# DeepFace downloads model weights at runtime; pre-create the cache dir
RUN mkdir -p /root/.deepface/weights

EXPOSE 8000

# Gunicorn is recommended for production; adjust `myproject` to your Django project name
CMD ["gunicorn", "myproject.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "2", \
    "--timeout", "120", \
    "--log-level", "info"]