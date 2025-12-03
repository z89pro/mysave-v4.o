# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# FINAL ARCHITECTURE: Manual Command Registration
# ============================================

import threading
import asyncio
import logging
import os
import pyromod  # Crucial for /cookie

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from config.settings import API_ID, API_HASH, BOT_TOKEN, MONGO_DB
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from app import app

# --- Import Commands Manually ---
from commands.yt import yt_command, yt_callback
from commands.i import insta_command
from commands.cookies import cookie_command
from commands.help import help_command, help_callback
from commands.status import status_command
from commands.usage import usage_command
from commands.recover import recover_command

# -------------------------------------------------
# Logging & Database
# -------------------------------------------------
logging.getLogger("pyrogram").setLevel(logging.INFO)
logger = get_logger()

# 5-second timeout to prevent "freezing" if IP is bad
db_client = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
db = db_client["savebot"]
users_col = db["users"]

# -------------------------------------------------
# Initialize Client
# -------------------------------------------------
# Note: We removed 'plugins=...' because we are registering manually below
bot = Client("ZainBotV4", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -------------------------------------------------
# DB Wrappers (For commands needing 'db')
# -------------------------------------------------
async def status_wrapper(client, message):
    await status_command(client, message, db)

async def usage_wrapper(client, message):
    await usage_command(client, message, db)

async def recover_wrapper(client, message):
    await recover_command(client, message, db)

# -------------------------------------------------
# Register Handlers (The "Wiring")
# -------------------------------------------------
def register_commands(app):
    # /start
    app.add_handler(MessageHandler(start_handler, filters.command("start")))
    
    # /yt
    app.add_handler(MessageHandler(yt_command, filters.command("yt")))
    app.add_handler(CallbackQueryHandler(yt_callback, filters.regex("^yt_")))

    # /i (Instagram)
    app.add_handler(MessageHandler(insta_command, filters.command("i")))

    # /cookie
    app.add_handler(MessageHandler(cookie_command, filters.command("cookie")))

    # /help
    app.add_handler(MessageHandler(help_command, filters.command("help")))
    app.add_handler(CallbackQueryHandler(help_callback, filters.regex("^help_")))

    # /status, /usage, /recover (Wrapped with DB)
    app.add_handler(MessageHandler(status_wrapper, filters.command("status")))
    app.add_handler(MessageHandler(usage_wrapper, filters.command("usage")))
    app.add_handler(MessageHandler(recover_wrapper, filters.command("recover")))

    logger.success("✅ All commands registered successfully!")

# -------------------------------------------------
# /start Handler
# -------------------------------------------------
async def start_handler(client, message):
    status_msg = await message.reply_text("⚡ **Bot is Online!** Checking Database...")
    try:
        user_id = message.from_user.id
        if not await users_col.find_one({"user_id": user_id}):
            await users_col.insert_one({"user_id": user_id})

        await status_msg.edit_text(
            f"👋 Hello {message.from_user.mention}!\n\n"
            f"🤖 **Save Restricted Content Bot v4**\n"
            f"⚡ *Powered by Zain*\n\n"
            f"✅ **System Fully Operational**\n"
            f"🎬 `/yt <link>` — YouTube\n"
            f"📸 `/i <link>` — Instagram\n"
            f"🍪 `/cookie` — Login"
        )
    except Exception as e:
        logger.error(f"❌ DB Error: {e}")
        await status_msg.edit_text(f"⚠️ **Database Error**\n`{e}`")

# -------------------------------------------------
# Run Bot + Web
# -------------------------------------------------
def run_bot():
    asyncio.run(start_bot())

async def start_bot():
    register_exit_cleanup()
    startup_cleanup_banner()
    
    # Register commands BEFORE starting
    register_commands(bot)

    logger.info("⏳ Connecting to Telegram...")
    await bot.start()
    
    me = await bot.get_me()
    logger.success(f"✅ Connected as @{me.username}")
    logger.success("✅ Bot started. Send /start or /yt to test.")

    # Safe Infinite Loop
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
