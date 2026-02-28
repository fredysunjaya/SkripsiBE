# syntax=docker/dockerfile:1

# Base image with minimal footprint
FROM python:3.13-slim AS base

# keep output unbuffered and bytecode generation off
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# install build and runtime dependencies
RUN apt-get update && apt-get install -y \
        gcc \
        libpq-dev \
        build-essential \
        libxcb1 libxcb-render0 libxcb-shm0 libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy and install python requirements first so layer can be cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the code
COPY . .

# collect static assets during build
RUN python manage.py collectstatic --noinput


# final stage (could be the same as base for a simple project)
FROM base AS final
WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=skripsiBE.settings

EXPOSE 8080

# use gunicorn with an async uvicorn worker for ASGI compatibility
CMD ["gunicorn", "skripsiBE.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8080"]
