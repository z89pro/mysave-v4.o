
# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/usage.py
# Description: Show total file and data usage for premium or admin users
# ============================================

import humanize
from config.settings import OWNER_ID
from premium import is_premium

async def usage_command(client, message, db):
    """
    Display the user's usage stats: total files processed and data size.
    Only accessible to premium users or the bot owner.
    """
    user_id = message.from_user.id
    user = await db["users"].find_one({"user_id": user_id}) or {}
    usage = user.get("usage", {"files": 0, "bytes": 0})

    is_owner = user_id == OWNER_ID
    if not (await is_premium(user_id) or is_owner):
        return await message.reply("🔒 Usage stats are available for Premium users only.")

    text = (
        f"📊 **Usage Summary**\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"📦 Files processed: **{usage['files']}**\n"
        f"💾 Data used: **{humanize.naturalsize(usage['bytes'])}**\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"⚡ Powered by Zain"
    )

    await message.reply(text)
