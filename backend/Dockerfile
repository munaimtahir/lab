FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files (creates /app/staticfiles with Django admin CSS/JS)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Run migrations, seed data, and start gunicorn bound to 0.0.0.0
CMD python manage.py migrate && \
    python manage.py seed_data && \
    gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers ${WORKERS:-$((2 * $(nproc) + 1))} --timeout 120 --access-logfile - --error-logfile -
