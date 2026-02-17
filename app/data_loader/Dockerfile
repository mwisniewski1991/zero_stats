FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy into data_loader subdir so "python -m data_loader.run_loader" resolves relative imports
COPY . /app/data_loader
WORKDIR /app

CMD ["python", "-m", "data_loader.run_loader", "--check"]
