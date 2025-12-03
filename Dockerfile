# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: Dockerfile
# Description: Container setup for Koyeb / Render / Heroku
# ============================================

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["bash", "-c", "python3 main.py & python3 app.py"]
