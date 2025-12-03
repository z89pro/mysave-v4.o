# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/cookies.py
# Description: /cookie command — handle YouTube and Instagram cookie uploads
# ============================================

from pyrogram import filters
from utils.safe_send import safe_send
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

# MongoDB connection for storing user cookies
db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

# --------------------------------------------
# /cookie Command Handler
# --------------------------------------------

async def cookie_command(client, message):
    """
    Wait for a user to send cookie.txt after /cookie command.
    Automatically detects whether the cookie is for YouTube or Instagram.
    Stores it permanently for the user.
    """
    await message.reply_text(
        "📥 Please send your `cookie.txt` file (from YouTube or Instagram).",
        quote=True,
    )

    # Wait for the next document upload by this user
    response = await client.listen(filters.user(message.from_user.id) & filters.document, timeout=120)
    if not response:
        return await message.reply("⏰ Timeout — No file received within 2 minutes.")

    doc = response.document
    if not doc.file_name.endswith(".txt"):
        return await message.reply("❌ Invalid file format. Please send a `.txt` file.")

    file_path = await client.download_media(doc)
    cookie_text = open(file_path, "r", encoding="utf-8").read()

    # Auto-detect service type
    detected = None
    if "youtube.com" in cookie_text or "YSC" in cookie_text:
        detected = "yt"
    elif "instagram.com" in cookie_text or "csrftoken" in cookie_text:
        detected = "insta"

    if not detected:
        return await message.reply("❌ Could not detect whether the cookie is for YouTube or Instagram.")

    user_id = message.from_user.id
    user = await user_cookies.find_one({"user_id": user_id}) or {"user_id": user_id}

    if detected == "yt":
        user["yt_cookie"] = cookie_text
        msg = "✅ YouTube cookies saved successfully!"
    elif detected == "insta":
        user["insta_cookie"] = cookie_text
        msg = "✅ Instagram cookies saved successfully!"

    await user_cookies.update_one({"user_id": user_id}, {"$set": user}, upsert=True)
    await safe_send(message.reply_text, f"{msg}\n⚡ Cookies stored permanently for your account.\n⚙️ Powered by Zain.")
