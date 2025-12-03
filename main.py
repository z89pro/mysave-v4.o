# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: main.py
# Description: Telegram bot entry point — initializes Pyrogram client, cleanup, and event loop
# ============================================

import asyncio
from pyrogram import Client, filters
from config.settings import API_ID, API_HASH, BOT_TOKEN
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger

# Initialize logger
logger = get_logger()

# Register cleanup functions
register_exit_cleanup()
startup_cleanup_banner()

# Initialize bot client
bot = Client(
    "ZainBotV4",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# --------------------------------------------
# Startup Message
# --------------------------------------------
@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\n"
        f"🤖 **Save Restricted Content Bot v4**\n"
        f"⚡ *Powered by Zain*\n\n"
        f"Use /help to explore all features."
    )

# --------------------------------------------
# Import Commands (you can map more commands here)
# --------------------------------------------
from commands.help import help_command
from commands.status import status_command
from commands.usage import usage_command
from commands.recover import recover_command
from premium import is_premium

@bot.on_message(filters.command("help"))
async def help_handler(client, message):
    await help_command(client, message)

@bot.on_message(filters.command("status"))
async def status_handler(client, message):
    from motor.motor_asyncio import AsyncIOMotorClient
    from config.settings import MONGO_DB
    db = AsyncIOMotorClient(MONGO_DB)["savebot"]
    await status_command(client, message, db)

@bot.on_message(filters.command("usage"))
async def usage_handler(client, message):
    from motor.motor_asyncio import AsyncIOMotorClient
    from config.settings import MONGO_DB
    db = AsyncIOMotorClient(MONGO_DB)["savebot"]
    await usage_command(client, message, db)

@bot.on_message(filters.command("recover"))
async def recover_handler(client, message):
    from motor.motor_asyncio import AsyncIOMotorClient
    from config.settings import MONGO_DB
    db = AsyncIOMotorClient(MONGO_DB)["savebot"]
    await recover_command(client, message, db)

# --------------------------------------------
# Bot Launcher
# --------------------------------------------
async def run_bot():
    logger.info("🚀 Launching Save Restricted Bot v4 — Powered by Zain")
    await bot.start()
    logger.success("✅ Bot started successfully.")
    await idle()  # Keeps the bot running
    await bot.stop()
    logger.warning("🛑 Bot stopped.")

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(run_bot())

