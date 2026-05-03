FROM python:3.11-slim

LABEL maintainer="NEXUS Ultimate Team <nexus@example.com>"
LABEL description="NEXUS Ultimate - Elite Cognitive AI Agent"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 nexus && \
    chown -R nexus:nexus /app
USER nexus

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from nexus import NexusAgent; print('healthy')"

# Default command
CMD ["python", "-m", "nexus.cli"]
