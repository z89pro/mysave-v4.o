# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: main.py
# Description: Telegram bot entry point — now broadcasts startup message to all users
# ============================================

import asyncio
from pyrogram import Client, filters
from config.settings import API_ID, API_HASH, BOT_TOKEN
from utils.cleanup import startup_cleanup_banner, register_exit_cleanup
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB, OWNER_ID
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated

# --------------------------------------------
# Setup
# --------------------------------------------
logger = get_logger()
register_exit_cleanup()
startup_cleanup_banner()

# Initialize MongoDB
db_client = AsyncIOMotorClient(MONGO_DB)
db = db_client["savebot"]
users_col = db["users"]

# Initialize Pyrogram bot
bot = Client(
    "ZainBotV4",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# --------------------------------------------
# START Command
# --------------------------------------------
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
        f"Use /help to explore features.\n\n"
        f"🎬 `/yt <link>` — Download from YouTube\n"
        f"📸 `/i <link>` — Download from Instagram\n"
        f"🍪 `/cookie` — Set your cookies"
    )

# --------------------------------------------
# HELP, STATUS, USAGE, RECOVER Commands
# --------------------------------------------
from commands.help import help_command
from commands.status import status_command
from commands.usage import usage_command
from commands.recover import recover_command

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

# --------------------------------------------
# NEW COMMANDS — Downloader + Cookies
# --------------------------------------------
from commands.yt import yt_command, yt_callback
from commands.i import insta_command
from commands.cookies import cookie_command

# YouTube Downloader
@bot.on_message(filters.command("yt"))
async def yt_handler(client, message):
    await yt_command(client, message)

# Instagram Downloader
@bot.on_message(filters.command("i"))
async def insta_handler(client, message):
    await insta_command(client, message)

# Cookie Manager
@bot.on_message(filters.command("cookie"))
async def cookie_handler(client, message):
    await cookie_command(client, message)

# Inline Callback Handler for YouTube menu
@bot.on_callback_query(filters.regex("^yt_"))
async def yt_callback_handler(client, callback_query):
    await yt_callback(client, callback_query)

# --------------------------------------------
# BROADCAST ON STARTUP (SAFE MODE)
# --------------------------------------------

async def broadcast_startup_message():
    """Send a startup message to all users safely."""
    startup_text = (
        "✅ **Bot Started Successfully!**\n\n"
        "⚡ Save Restricted Bot v4 is now live.\n"
        "🎬 Use /yt <link> for YouTube\n"
        "📸 Use /i <link> for Instagram\n\n"
        "🚀 Powered by Zain"
    )

    count = 0
    failed = 0
    async for user in users_col.find():
        try:
            await bot.send_message(user["user_id"], startup_text)
            count += 1
            await asyncio.sleep(3)  # delay to prevent FloodWait
        except (UserIsBlocked, PeerIdInvalid, InputUserDeactivated):
            failed += 1
            continue
        except FloodWait as e:
            await asyncio.sleep(e.value + 5)
        except Exception as e:
            failed += 1
            logger.warning(f"Broadcast failed for {user['user_id']}: {e}")

    logger.success(f"📢 Startup broadcast completed — Sent: {count} | Failed: {failed}")

# --------------------------------------------
# BOT RUNNER
# --------------------------------------------
async def run_bot():
    logger.info("🚀 Launching Save Restricted Bot v4 — Powered by Zain")
    await bot.start()
    logger.success("✅ Bot started successfully and is ready to use.")

    # Broadcast after startup
    await broadcast_startup_message()

    # Notify owner
    try:
        await bot.send_message(OWNER_ID, "📢 Broadcast sent to all users.\n⚡ Powered by Zain")
    except Exception as e:
        logger.warning(f"Could not message owner: {e}")

    from pyrogram import idle
    await idle()
    await bot.stop()
    logger.warning("🛑 Bot stopped.")

if __name__ == "__main__":
    asyncio.run(run_bot())
