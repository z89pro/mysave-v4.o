# ------------------------------
# ⚡ Save Restricted Bot v4 — Zain Edition
# ------------------------------
FROM python:3.11-slim

WORKDIR /app

# copy files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose dashboard port
EXPOSE 5000

# cleanup logs weekly
ENV PYTHONUNBUFFERED=1

CMD ["bash", "-c", "python3 main.py & python3 app.py"]
