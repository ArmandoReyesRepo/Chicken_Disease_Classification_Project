# Use official Python 3.11 slim image (compatible with TensorFlow)
FROM python:3.11-slim-bullseye

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        awscli \
        build-essential \
        gcc \
        g++ \
        gfortran \
        libpq-dev \
        libffi-dev \
        libssl-dev \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        wget \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app.py"]

