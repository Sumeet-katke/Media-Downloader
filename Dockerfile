# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (for caching)
COPY requirements.txt .

# 5. Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy rest of project
COPY . .

# 7. Expose port
EXPOSE 5000

# 8. Run app
CMD ["python", "AMD/app.py"]