FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Prometheus Flask exporter explicitly
RUN pip install --no-cache-dir prometheus-flask-exporter==0.22.3

# Copy the entire application
COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use Gunicorn with proper configuration
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--timeout=120", "--log-level=info", "run:app"]
