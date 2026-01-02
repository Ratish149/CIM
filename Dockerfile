# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt
# Set PATH to use virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy project code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create media and static directories
RUN mkdir -p /app/media

# Expose port
EXPOSE 8000

# Run server
CMD ["sh", "-c", "python manage.py migrate && gunicorn CIM.wsgi:application --bind 0.0.0.0:8000"]
