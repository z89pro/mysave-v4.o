
# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/status.py
# Description: Show system and bot status with user statistics
# ============================================

import platform
import psutil
import datetime
from config.settings import VERSION

async def status_command(client, message, db):
    """
    Display real-time bot statistics and system status.
    """
    users = await db["users"].estimated_document_count()
    premium = await db["premium_users"].estimated_document_count()
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    text = (
        f"🩺 **System Status**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 **Bot Version:** {VERSION}\n"
        f"👥 **Users:** {users}\n"
        f"💎 **Premium:** {premium}\n"
        f"🧠 **CPU:** {cpu}% | 💾 **RAM:** {mem}%\n"
        f"⏱ **Uptime:** {str(uptime).split('.')[0]}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ *Powered by Zain*"
    )

    await message.reply_text(text)
