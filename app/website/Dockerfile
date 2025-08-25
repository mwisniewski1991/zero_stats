FROM python:3.11-slim

# Set working directory
WORKDIR /app


# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 34576

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:34576/ || exit 1

# Ustawiamy zmienne środowiskowe
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=production

CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]