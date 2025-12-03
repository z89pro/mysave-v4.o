# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# Fix: Thread-safe bot loop + Dynamic Port Handling
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
async def start_handler(_, message):
    user_id = message.from_user.id
    if not await users_col.find_one({"user_id": user_id}):
        await users_col.insert_one({"user_id": user_id})
    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\n"
        f"🤖 **Save Restricted Content Bot v4**\n"
        f"⚡ *Powered by Zain*\n\n"
        f"🎬 `/yt <link>` — Download from YouTube\n"
        f"📸 `/i <link>` — Download from Instagram\n"
        f"🍪 `/cookie` — Set your cookies"
    )

@bot.on_message()
async def debug_all(_, message):
    pass

# -------------------------------------------------
# Run the bot (Thread-Safe)
# -------------------------------------------------
def run_bot():
    """Entry point for the background thread."""
    asyncio.run(start_bot())

async def start_bot():
    """Start the bot safely without using signals."""
    register_exit_cleanup()
    startup_cleanup_banner()

    await bot.start()
    me = await bot.get_me()
    logger.success(f"✅ Connected as @{me.username}")
    logger.success("✅ Bot started successfully and is ready to use.")

    # CRITICAL FIX: Use infinite sleep instead of idle() to prevent threading crash
    while True:
        await asyncio.sleep(3600)

# -------------------------------------------------
# Run Flask (Main Thread) + Bot (Background)
# -------------------------------------------------
if __name__ == "__main__":
    # 1. Start the Telegram bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # 2. Run the Flask dashboard in the Main Thread
    # Fix: Use os.getenv("PORT") to satisfy Render/Koyeb health checks
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
