# ------------------------------
# Stage 1: Builder
# ------------------------------
FROM python:3.11-bullseye AS builder

# Install system dependencies for building packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
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

# Copy app files
COPY . /app

# Install all Python dependencies in one go
RUN pip install --prefix=/install --no-cache-dir --no-build-isolation \
    tensorflow==2.13.0 \
    numpy pandas scipy matplotlib seaborn notebook dvc python-box==6.0.2 \
    pyYAML tqdm ensure==1.0.2 joblib Flask Flask-Cors -e .

# ------------------------------
# Stage 2: Final image
# ------------------------------
FROM python:3.11-slim-bullseye

# Minimal runtime dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        awscli \
        libpq-dev \
        libssl-dev \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY . /app

# Expose port for Flask app
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
