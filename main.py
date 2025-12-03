# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# Fix: Added Debugging to find the "No Response" cause
# ============================================

import threading
import asyncio
import logging
import os
from pyrogram import Client, filters
from config.settings import API_ID, API_HASH, BOT_TOKEN, MONGO_DB
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from app import app

# -------------------------------------------------
# Logging setup
# -------------------------------------------------
logging.getLogger("pyrogram").setLevel(logging.INFO)
logger = get_logger()

# -------------------------------------------------
# MongoDB setup
# -------------------------------------------------
# Print DB status to logs
if not MONGO_DB:
    logger.error("❌ MONGO_DB variable is missing! The bot will hang.")
else:
    logger.info("✅ MONGO_DB variable is present. Attempting connection...")

db_client = AsyncIOMotorClient(MONGO_DB)
db = db_client["savebot"]
users_col = db["users"]

# -------------------------------------------------
# Initialize Pyrogram client
# -------------------------------------------------
bot = Client("ZainBotV4", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -------------------------------------------------
# Telegram commands
# -------------------------------------------------
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    # 1. IMMEDIATE REPLY (To confirm bot is receiving messages)
    status_msg = await message.reply_text(f"⚡ Connected! Checking Database for {message.from_user.first_name}...")

    try:
        # 2. Database Check (This is likely where it hangs)
        user_id = message.from_user.id
        if not await users_col.find_one({"user_id": user_id}):
            await users_col.insert_one({"user_id": user_id})
        
        # 3. Success Reply
        await status_msg.edit_text(
            f"👋 Hello {message.from_user.mention}!\n\n"
            f"🤖 **Save Restricted Content Bot v4**\n"
            f"✅ **Database Connected Successfully**\n"
            f"⚡ *Powered by Zain*\n\n"
            f"🎬 `/yt <link>` — Download from YouTube\n"
            f"📸 `/i <link>` — Download from Instagram\n"
        )
    except Exception as e:
        # 4. Error Reply
        logger.error(f"Database Error: {e}")
        await status_msg.edit_text(f"❌ **Database Error:**\n`{str(e)}`\n\nCheck your MONGO_DB variable in Koyeb settings.")

@bot.on_message()
async def debug_all(_, message):
    """Log every message received to console to verify connection."""
    print(f"📩 DEBUG: Received message from {message.from_user.id}: {message.text}")

# -------------------------------------------------
# Run the bot (Thread-Safe)
# -------------------------------------------------
def run_bot():
    asyncio.run(start_bot())

async def start_bot():
    register_exit_cleanup()
    startup_cleanup_banner()
    await bot.start()
    me = await bot.get_me()
    logger.success(f"✅ Connected as @{me.username}")
    logger.success("✅ Bot started successfully. Waiting for messages...")
    while True:
        await asyncio.sleep(3600)

# -------------------------------------------------
# Run Flask (Main Thread) + Bot (Background)
# -------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
