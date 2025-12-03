
# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: app.py
# Description: Flask-based web dashboard and admin API
# ============================================

import os
import datetime
from flask import Flask, render_template
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB, VERSION

# Initialize Flask app and MongoDB
app = Flask(__name__)
client = AsyncIOMotorClient(MONGO_DB)
db = client["savebot"]

@app.route("/")
def welcome():
    """
    Web dashboard homepage.
    Displays the Zain-branded welcome page.
    """
    return render_template(
        "welcome.html",
        version=VERSION,
        year=datetime.datetime.now().year,
    )

@app.route("/spy_admin")
async def spy_admin():
    """
    Returns JSON stats for total and premium users.
    Accessible only to the owner (use API authentication if exposed).
    """
    users = await db["users"].estimated_document_count()
    premium = await db["premium_users"].estimated_document_count()
    return {
        "bot_version": VERSION,
        "total_users": users,
        "premium_users": premium,
        "status": "✅ Online",
        "powered_by": "Zain",
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
