import threading
import asyncio
import logging
import os
import pyromod  # REQUIRED: Patches Pyrogram

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import API_ID, API_HASH, BOT_TOKEN, MONGO_DB
from utils.logger import get_logger
from app import app

# Import Commands
from commands.yt import yt_command, yt_callback
from commands.i import insta_command
from commands.cookies import cookie_command
from commands.help import help_command

# Logger Init
logger = get_logger()

# DB Init (Low Timeout to prevent hanging)
db_client = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
db = db_client["savebot"]

# Client Init
bot = Client("ZainBotFinal", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Handlers ---

async def start_handler(client, message):
    logger.info(f"📩 RECEIVED START from {message.from_user.id}")
    msg = await message.reply("⚡ Connecting...")
    try:
        # Test DB
        await db.command("ping")
        await msg.edit("✅ **Bot Online & DB Connected!**\n\nTry `/yt <link>`")
    except Exception as e:
        await msg.edit(f"❌ **DB Error:** {e}")

async def debug_handler(client, message):
    # This proves the bot "hears" even if it doesn't reply
    logger.info(f"👂 HEARD MESSAGE: {message.text}")

# --- Registration ---

def register_handlers(app):
    # Debug Listener (Catches all text)
    app.add_handler(MessageHandler(debug_handler, filters.text), group=-1)

    # Commands
    app.add_handler(MessageHandler(start_handler, filters.command("start")))
    app.add_handler(MessageHandler(yt_command, filters.command("yt")))
    app.add_handler(CallbackQueryHandler(yt_callback, filters.regex("^yt_")))
    app.add_handler(MessageHandler(insta_command, filters.command("i")))
    app.add_handler(MessageHandler(cookie_command, filters.command("cookie")))
    app.add_handler(MessageHandler(help_command, filters.command("help")))
    
    logger.success("✅ Handlers Registered.")

# --- Run Loop ---

def run_bot_thread():
    asyncio.run(start_bot())

async def start_bot():
    logger.info("⏳ Initializing...")
    register_handlers(bot)
    
    await bot.start()
    
    # FORCE DELETE WEBHOOK (Fixes 'No Reply' issue)
    logger.info("🧹 Clearing Webhooks...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    me = await bot.get_me()
    logger.success(f"✅ Logged in as @{me.username}")
    
    # Infinite Sleep (Better than idle())
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # Bot Thread
    threading.Thread(target=run_bot_thread, daemon=True).start()
    
    # Web Thread
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
