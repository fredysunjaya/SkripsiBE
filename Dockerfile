# Use the official Python 3.13 slim image as a base
FROM python:3.13-slim

# Set environment variables to ensure Python outputs are not buffered
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y libxcb1 libxcb-render0 libxcb-shm0 libgl1-mesa-glx 
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory for your Django app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies from the requirements.txt
RUN pip install -r requirements.txt

# Copy the entire Django project code into the container
COPY . /app/

# Set the environment variable for Django's settings module
ENV DJANGO_SETTINGS_MODULE=skripsiBE.settings

# Collect static files (optional if you need static files in production)
RUN python manage.py collectstatic --noinput

# Expose the port that Uvicorn will run on
EXPOSE 8080

# Command to run the application using Uvicorn and Gunicorn
# CMD ["python", "-m", "gunicorn", "skripsiBE.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8080"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]