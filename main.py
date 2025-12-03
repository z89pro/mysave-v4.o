# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: main.py
# Description: Single Render Free Service (Flask + Bot)
# ============================================

import threading
import asyncio
import logging
from pyrogram import Client, filters, idle
from app import app
from config.settings import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_DB
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient

# -------------------------------------------------
# Logging setup
# -------------------------------------------------
logging.getLogger("pyrogram").setLevel(logging.INFO)
logger = get_logger()

# -------------------------------------------------
# Flask background thread (different port)
# -------------------------------------------------
def run_web():
    """Run Flask dashboard in background thread."""
    # changed port to 11000 to avoid Render conflict
    app.run(host="0.0.0.0", port=11000)

threading.Thread(target=run_web, daemon=True).start()

# -------------------------------------------------
# MongoDB setup
# -------------------------------------------------
db_client = AsyncIOMotorClient(MONGO_DB)
db = db_client["savebot"]
users_col = db["users"]

# -------------------------------------------------
# Cleanup tasks
# -------------------------------------------------
register_exit_cleanup()
startup_cleanup_banner()

# -------------------------------------------------
# Initialize Pyrogram Client
# -------------------------------------------------
bot = Client("ZainBotV4", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -------------------------------------------------
# Debug listener
# -------------------------------------------------
@bot.on_message()
async def debug_all(_, message):
    print(f"DEBUG UPDATE RECEIVED: {message.text}")

# -------------------------------------------------
# Command: /start
# -------------------------------------------------
@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    user_id = message.from_user.id
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        await users_col.insert_one({"user_id": user_id})

    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\n"
        f"🤖 **Save Restricted Content Bot v4**\n"
        f"⚡ *Powered by Zain*\n\n"
        f"🎬 `/yt <link>` — Download from YouTube\n"
        f"📸 `/i <link>` — Download from Instagram\n"
        f"🍪 `/cookie` — Set your cookies"
    )

# -------------------------------------------------
# Import other commands
# -------------------------------------------------
from commands.help import help_command
from commands.status import status_command
from commands.usage import usage_command
from commands.recover import recover_command
from commands.yt import yt_command, yt_callback
from commands.i import insta_command
from commands.cookies import cookie_command

@bot.on_message(filters.command("help"))
async def help_handler(client, message):
    await help_command(client, message)

@bot.on_message(filters.command("status"))
async def status_handler(client, message):
    await status_command(client, message, db)

@bot.on_message(filters.command("usage"))
async def usage_handler(client, message):
    await usage_command(client, message, db)

@bot.on_message(filters.command("recover"))
async def recover_handler(client, message):
    await recover_command(client, message, db)

@bot.on_message(filters.command("yt"))
async def yt_handler(client, message):
    await yt_command(client, message)

@bot.on_message(filters.command("i"))
async def insta_handler(client, message):
    await insta_command(client, message)

@bot.on_message(filters.command("cookie"))
async def cookie_handler(client, message):
    await cookie_command(client, message)

@bot.on_callback_query(filters.regex("^yt_"))
async def yt_callback_handler(client, callback_query):
    await yt_callback(client, callback_query)

# -------------------------------------------------
# Main runner
# -------------------------------------------------
async def main():
    logger.info("🚀 Launching Save Restricted Bot v4 — Powered by Zain")
    await bot.start()
    me = await bot.get_me()
    print(f"Connected as @{me.username}")
    logger.success("✅ Bot started successfully and is ready to use.")

    await idle()
    await bot.stop()
    logger.warning("🛑 Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
