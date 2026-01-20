# Build stage
FROM python:3.11-slim

# Install system dependencies
# git: for pip installs if needed
# build-essential: for compiling some python extensions
# curl: for healthchecks
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

    # Upgrade pip to handle SSL/timeouts better
    RUN pip install --upgrade pip

    # Install dependencies individually to handle network instability
    # Use high timeout and retries
    COPY requirements.txt .
    RUN pip install --no-cache-dir --default-timeout=100 --retries 10 requests && \
        pip install --no-cache-dir --default-timeout=100 --retries 10 pathway && \
        pip install --no-cache-dir --default-timeout=100 --retries 10 "google-generativeai>=0.7.0" && \
        pip install --no-cache-dir --default-timeout=100 --retries 10 python-dotenv && \
        pip install --no-cache-dir --default-timeout=100 --retries 10 streamlit && \
        pip install --no-cache-dir --default-timeout=100 --retries 10 pandas

# Copy the rest of the application
COPY . .

# Environment variables
# (Do not bake secrets here; pass them at runtime via --env-file)
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Copy and set entrypoint
COPY launcher.py .

# Use python launcher as the supervisor
ENTRYPOINT ["python", "launcher.py"]
