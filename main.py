# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# FINAL PRODUCTION BUILD
# Includes: Thread Fix, Webhook Fix, and DB Timeout Protection
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
# MongoDB setup (With Timeout Protection)
# -------------------------------------------------
# serverSelectionTimeoutMS=5000 prevents the bot from hanging if IP is bad
db_client = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
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
    # 1. Send "Processing..." immediately so you know the bot heard you
    status_msg = await message.reply_text("⚡ Connecting to Database...")

    try:
        user_id = message.from_user.id
        
        # 2. Try to verify user in DB (This will fail fast if DB is bad)
        if not await users_col.find_one({"user_id": user_id}):
            await users_col.insert_one({"user_id": user_id})

        # 3. Success!
        await status_msg.edit_text(
            f"👋 Hello {message.from_user.mention}!\n\n"
            f"🤖 **Save Restricted Content Bot v4**\n"
            f"⚡ *Powered by Zain*\n\n"
            f"🎬 `/yt <link>` — Download from YouTube\n"
            f"📸 `/i <link>` — Download from Instagram\n"
            f"🍪 `/cookie` — Set your cookies"
        )
        logger.info(f"✅ User {user_id} started the bot.")

    except Exception as e:
        # 4. Catch DB Errors
        logger.error(f"❌ DB Error: {e}")
        error_text = (
            f"❌ **Database Connection Failed**\n\n"
            f"**Reason:** `{str(e)}`\n\n"
            f"**Fix:** Go to MongoDB Atlas > Network Access > Add IP `0.0.0.0/0`"
        )
        await status_msg.edit_text(error_text)

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

    logger.info("⏳ Starting Bot...")
    await bot.start()
    
    me = await bot.get_me()
    logger.success(f"✅ Connected as @{me.username}")
    logger.success("✅ Bot started successfully. Send /start to test.")

    # Prevent threading crash by using infinite sleep instead of idle()
    while True:
        await asyncio.sleep(3600)

# -------------------------------------------------
# Run Flask (Main Thread) + Bot (Background)
# -------------------------------------------------
if __name__ == "__main__":
    # 1. Start the Telegram bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # 2. Run the Flask dashboard in the Main Thread
    port = int(os.getenv("PORT", 8080))
    # We turn off Flask debug mode for production safety
    app.run(host="0.0.0.0", port=port, debug=False)
