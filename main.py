# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# FINAL FIX: Loads Plugins, Debugs Updates, Fixes Threads
# ============================================

import threading
import asyncio
import logging
import os
from pyrogram import Client, filters, idle
from config.settings import API_ID, API_HASH, BOT_TOKEN, MONGO_DB
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from app import app
import pyromod  # Needed for client.listen in cookies.py

# -------------------------------------------------
# Logging setup
# -------------------------------------------------
logging.getLogger("pyrogram").setLevel(logging.INFO)
logger = get_logger()

# -------------------------------------------------
# MongoDB setup (With 5s Timeout to prevent freezing)
# -------------------------------------------------
db_client = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
db = db_client["savebot"]
users_col = db["users"]

# -------------------------------------------------
# Initialize Pyrogram client
# -------------------------------------------------
# FIX: Added plugins=dict(root="commands") to load /yt, /help, etc.
bot = Client(
    "ZainBotV4", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN,
    plugins=dict(root="commands") 
)

# -------------------------------------------------
# DEBUG HANDLER: Prove Connectivity
# -------------------------------------------------
@bot.on_message(group=-1)
async def log_everything(client, message):
    """
    This runs for EVERY message. 
    Check your logs for '📩 I HEARD YOU' to prove the bot is listening.
    """
    logger.info(f"📩 I HEARD YOU! Message from: {message.from_user.first_name} (ID: {message.from_user.id})")

# -------------------------------------------------
# /start Handler (Database Check)
# -------------------------------------------------
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    # 1. Immediate Reply
    status_msg = await message.reply_text("⚡ **Bot is Online!** Checking Database...")

    try:
        user_id = message.from_user.id
        
        # 2. Database Handshake
        if not await users_col.find_one({"user_id": user_id}):
            await users_col.insert_one({"user_id": user_id})

        # 3. Success
        await status_msg.edit_text(
            f"👋 Hello {message.from_user.mention}!\n\n"
            f"🤖 **Save Restricted Content Bot v4**\n"
            f"⚡ *Powered by Zain*\n\n"
            f"✅ **Database Connected**\n"
            f"✅ **Commands Loaded**\n\n"
            f"🎬 `/yt <link>` — YouTube\n"
            f"📸 `/i <link>` — Instagram\n"
            f"🍪 `/cookie` — Login"
        )
    except Exception as e:
        logger.error(f"❌ DB Error: {e}")
        await status_msg.edit_text(
            f"⚠️ **Database Error**\n\n"
            f"The bot is online, but cannot save users.\n"
            f"Error: `{e}`\n\n"
            f"**Fix:** Allow IP `0.0.0.0/0` in MongoDB Atlas Network Access."
        )

# -------------------------------------------------
# Run the bot (Thread-Safe)
# -------------------------------------------------
def run_bot():
    asyncio.run(start_bot())

async def start_bot():
    register_exit_cleanup()
    startup_cleanup_banner()

    logger.info("⏳ Starting Bot and Loading Plugins...")
    await bot.start()
    
    me = await bot.get_me()
    logger.success(f"✅ Connected as @{me.username}")
    logger.success("✅ Bot started successfully. Plugins loaded.")

    # Keep alive loop
    while True:
        await asyncio.sleep(3600)

# -------------------------------------------------
# Run Flask (Main) + Bot (Background)
# -------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
