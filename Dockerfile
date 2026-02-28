# syntax=docker/dockerfile:1

# Base image with minimal footprint
FROM python:3.13

# -----------------------------------
# switch to application directory
WORKDIR /app

# install build and runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/* 

# copy and install python requirements first so layer can be cached
COPY requirements.txt .
# copy the rest of the code
COPY . .

# install dependencies - deepface with these dependency versions is working
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r /app/requirements_local.txt
# install deepface from source code (always up-to-date)
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -e . --no-deps

# collect static assets during build
RUN python manage.py collectstatic --noinput

# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8080

# use gunicorn with an async uvicorn worker for ASGI compatibility
CMD ["gunicorn", "skripsiBE.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8080"]
