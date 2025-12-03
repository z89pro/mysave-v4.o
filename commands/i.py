# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/i.py
# Description: /i command handler for Instagram downloads (reels, posts, stories)
# ============================================

from pyrogram import filters
from utils.downloads.instagram import download_instagram
from utils.safe_send import safe_send
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

# MongoDB collection for per-user cookies
db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

# --------------------------------------------
# /i Command Handler
# --------------------------------------------

async def insta_command(client, message):
    """
    Handle /i <link> command for downloading Instagram media.
    Supports reels, posts, and stories.
    """
    if len(message.command) < 2:
        return await safe_send(
            message.reply_text,
            "❌ Please provide an Instagram link.\nExample: `/i <link>`",
        )

    url = message.command[1]
    user_id = message.from_user.id

    # Fetch user’s stored Instagram cookie (if available)
    user = await user_cookies.find_one({"user_id": user_id})
    insta_cookie = user["insta_cookie"] if user and "insta_cookie" in user else None

    await download_instagram(client, message, url, cookie_data=insta_cookie)
