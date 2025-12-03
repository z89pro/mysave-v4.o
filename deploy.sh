#!/bin/bash
# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: deploy.sh
# Description: Auto-detect and deploy to Render, Koyeb, Heroku, or local
# ============================================

echo "🚀 Save Restricted Bot v4 — Powered by Zain"
echo "🔍 Detecting deployment environment..."

if [ -n "$RENDER_SERVICE_ID" ]; then
  echo "🟩 Detected Render Environment"
  echo "📦 Building using render.yaml or Dockerfile..."
  pip install -r requirements.txt
  echo "✅ Render deploy complete. Bot and web running."

elif [ -n "$KOYEB_APP_ID" ]; then
  echo "🟦 Detected Koyeb Environment"
  echo "🐳 Building with Dockerfile..."
  pip install -r requirements.txt
  python3 main.py & python3 app.py
  echo "✅ Koyeb bot + web started successfully."

elif [ -n "$DYNO" ]; then
  echo "🟪 Detected Heroku Environment"
  echo "⚙️ Running Heroku Procfile..."
  if [ "$DYNO" == "worker.1" ]; then
    python3 main.py
  else
    python3 app.py
  fi
  echo "✅ Heroku deploy complete."

else
  echo "💻 Local environment detected"
  echo "📦 Installing requirements..."
  pip install -r requirements.txt
  echo "🚀 Starting bot and dashboard locally..."
  python3 main.py & python3 app.py
  echo "✅ Running at http://127.0.0.1:10000"
fi
