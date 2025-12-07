# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH (correct location: /root/.local/bin)
ENV PATH="/root/.local/bin:${PATH}"

# Verify UV installation
RUN uv --version

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies with UV
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/models /app/output

# Expose port 8000
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_SYSTEM_PYTHON=1

# Run uvicorn with multiple workers for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]