FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (FFmpeg is REQUIRED for yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Standard for cloud apps)
EXPOSE 8080

# Run main.py which handles BOTH Bot and Web
CMD ["python3", "main.py"]
