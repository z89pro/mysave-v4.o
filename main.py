# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# Fix: Replaced pyrogram.idle() with asyncio.sleep() to fix threading crash
# ============================================

import threading
import asyncio
import logging
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
    """Print all received messages in logs (for debugging)."""
    # Optional: Comment out in production to reduce log noise
    # print(f"DEBUG UPDATE RECEIVED: {message.text}")
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

    # CRITICAL FIX: Do NOT use await idle() here. 
    # idle() uses signals which fail in a background thread.
    # Use an infinite sleep loop instead.
    while True:
        await asyncio.sleep(60)

# -------------------------------------------------
# Run Flask (main) + Bot (background)
# -------------------------------------------------
if __name__ == "__main__":
    # 1. Start the Telegram bot in a detached background thread
    #    daemon=True ensures it dies when the main Flask app dies
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # 2. Run the Flask dashboard in the Main Thread
    #    This blocks execution, keeping the script alive
    app.run(host="0.0.0.0", port=10000)
