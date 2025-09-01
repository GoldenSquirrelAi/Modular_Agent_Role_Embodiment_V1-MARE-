# MARE System Docker Container
FROM python:3.9-slim

LABEL maintainer="MARE Development Team"
LABEL version="1.0.0"
LABEL description="MARE Protocol Implementation - Production Container"

# Set environment variables
ENV PYTHONPATH=/app/src
ENV MARE_ENV=production
ENV MARE_LOG_LEVEL=INFO

# Create app directory and user
WORKDIR /app
RUN groupadd -r mareuser && useradd -r -g mareuser mareuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY *.json ./
COPY demo_mare.py .
COPY mare_live_demo.py .
COPY mare_web_demo.py .
COPY mare_validation_suite.py .
COPY mare_benchmark_comparison.py .

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs && \
    chown -R mareuser:mareuser /app

# Switch to non-root user
USER mareuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python3 -c "import sys; sys.path.insert(0, '/app/src'); from mare import MARESystem; s=MARESystem(); h=s.get_system_health(); s.shutdown(); exit(0 if h['system_status']=='healthy' else 1)"

# Expose port for web interface (if added)
EXPOSE 8080

# Default command - run web demo
CMD ["python3", "mare_web_demo.py"]