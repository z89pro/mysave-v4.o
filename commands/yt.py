# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/yt.py
# Description: /yt command and inline menu handler for YouTube downloader
# ============================================

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.downloads.youtube import download_youtube
from utils.safe_send import safe_send
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

# MongoDB connection for cookies
db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

# --------------------------------------------
# /yt Command Handler
# --------------------------------------------

async def yt_command(client, message):
    """
    Handle /yt <link> command.
    Detect YouTube link and show inline menu for quality/audio selection.
    """
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a YouTube link.\nExample: `/yt <link>`", quote=True)

    url = message.command[1]
    user_id = message.from_user.id

    # Fetch user's saved cookie if available
    user = await user_cookies.find_one({"user_id": user_id})
    cookie_file = None
    if user and "yt_cookie" in user:
        cookie_file = f"cookies_{user_id}_yt.txt"
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(user["yt_cookie"])

    await download_youtube(client, message, url, cookie_file=cookie_file)

# --------------------------------------------
# Inline Callback Handler
# --------------------------------------------

async def yt_callback(client, callback_query: CallbackQuery):
    """
    Handle inline button selections for YouTube quality/audio.
    """
    data = callback_query.data
    user_id = callback_query.from_user.id

    # Verify callback belongs to the correct user
    if not str(user_id) in data:
        return await callback_query.answer("❌ Not your selection!", show_alert=True)

    # Parse callback data
    if "yt_audio" in data:
        quality = "audio"
    else:
        quality = data.split("_")[1].replace("p", "")

    # Retrieve original YouTube message text to extract URL
    msg = callback_query.message.reply_to_message
    if not msg or len(msg.command) < 2:
        return await callback_query.answer("⚠️ Original link not found.", show_alert=True)

    url = msg.command[1]

    # Load cookie again (if saved)
    user = await user_cookies.find_one({"user_id": user_id})
    cookie_file = None
    if user and "yt_cookie" in user:
        cookie_file = f"cookies_{user_id}_yt.txt"
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(user["yt_cookie"])

    await callback_query.answer(f"⏬ Downloading in {quality} quality...", show_alert=False)
    await download_youtube(client, callback_query.message, url, quality_choice=quality, cookie_file=cookie_file)
