# Dockerfile

FROM python:3.12-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent directly to terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker caching)
COPY requirements/ requirements/

RUN pip install --upgrade pip

RUN pip install -r requirements/development.txt

# Copy project files
COPY . .

# Entrypoint
RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["sh", "docker/entrypoint.sh"]