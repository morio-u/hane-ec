# Dockerfile
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app itself
COPY . .

# Default launch command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]