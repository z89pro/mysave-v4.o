import threading
import asyncio
import logging
import os
import pyromod  # Monkeypatches Pyrogram for .listen()

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import API_ID, API_HASH, BOT_TOKEN, MONGO_DB
from utils.logger import get_logger
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from app import app

# Import Commands
from commands.yt import yt_command, yt_callback
from commands.i import insta_command
from commands.cookies import cookie_command
from commands.help import help_command, help_callback
from commands.status import status_command
from commands.usage import usage_command
from commands.recover import recover_command

# Logging
logging.getLogger("pyrogram").setLevel(logging.INFO)
logger = get_logger()

# Database (Timeout set to 5s to prevent freezing)
db_client = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
db = db_client["savebot"]
users_col = db["users"]

# Client Init (No 'plugins' arg needed)
bot = Client("ZainBotV4", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Wrappers for DB Commands ---
async def status_wrapper(c, m): await status_command(c, m, db)
async def usage_wrapper(c, m): await usage_command(c, m, db)
async def recover_wrapper(c, m): await recover_command(c, m, db)

# --- Start Handler ---
async def start_handler(client, message):
    msg = await message.reply("⚡ Connecting...")
    try:
        user_id = message.from_user.id
        # Database Handshake
        if not await users_col.find_one({"user_id": user_id}):
            await users_col.insert_one({"user_id": user_id})
        
        await msg.edit(
            f"👋 **Hello {message.from_user.first_name}!**\n"
            f"✅ Bot is Online & Database Connected.\n\n"
            f"🎬 `/yt` - YouTube\n"
            f"📸 `/i` - Instagram\n"
            f"🍪 `/cookie` - Login"
        )
    except Exception as e:
        logger.error(f"DB Error: {e}")
        await msg.edit(f"❌ **Database Error:** {e}\nCheck IP Whitelist.")

# --- Registration Function ---
def register_all_handlers(app):
    # Basic Commands
    app.add_handler(MessageHandler(start_handler, filters.command("start")))
    app.add_handler(MessageHandler(yt_command, filters.command("yt")))
    app.add_handler(CallbackQueryHandler(yt_callback, filters.regex("^yt_")))
    app.add_handler(MessageHandler(insta_command, filters.command("i")))
    app.add_handler(MessageHandler(cookie_command, filters.command("cookie")))
    app.add_handler(MessageHandler(help_command, filters.command("help")))
    app.add_handler(CallbackQueryHandler(help_callback, filters.regex("^help_")))
    
    # DB Commands
    app.add_handler(MessageHandler(status_wrapper, filters.command("status")))
    app.add_handler(MessageHandler(usage_wrapper, filters.command("usage")))
    app.add_handler(MessageHandler(recover_wrapper, filters.command("recover")))
    
    logger.success("✅ All commands registered manually.")

# --- Execution ---
def run_bot():
    asyncio.run(start_bot_async())

async def start_bot_async():
    register_exit_cleanup()
    startup_cleanup_banner()
    register_all_handlers(bot)
    
    logger.info("⏳ Connecting to Telegram...")
    await bot.start()
    
    me = await bot.get_me()
    logger.success(f"✅ Logged in as @{me.username}")
    
    # Infinite Keep-Alive
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # Start Bot in Background Thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Start Web Server in Main Thread
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
