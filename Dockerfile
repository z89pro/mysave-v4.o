# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# Dockerfile for Render / Koyeb
# ============================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (FFmpeg is required for yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Render/Koyeb sets the PORT env var, but we expose a default just in case
EXPOSE 8080

# Run ONLY main.py (it now handles both Bot and Web)
CMD ["python3", "main.py"]
