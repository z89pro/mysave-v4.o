# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/help.py
# Description: Interactive help menu with inline buttons
# ============================================

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def help_command(client, message):
    """
    Display an interactive help menu with quick navigation buttons.
    """
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Download", callback_data="help_download"),
         InlineKeyboardButton("📦 Batch", callback_data="help_batch")],
        [InlineKeyboardButton("💎 Premium", callback_data="help_premium"),
         InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")],
        [InlineKeyboardButton("📊 Usage", callback_data="help_usage"),
         InlineKeyboardButton("♻️ Recover", callback_data="help_recover")]
    ])

    text = (
        "🤖 **Save Restricted Content Bot v4**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ *Powered by Zain*\n"
        "A professional Telegram bot to save restricted content, "
        "manage media downloads, and more.\n\n"
        "Use the buttons below to explore features 👇"
    )

    await message.reply_text(text, reply_markup=keyboard, parse_mode=enums.ParseMode.MARKDOWN)

# Optional callback handler (to display help topics dynamically)
async def help_callback(client, callback_query):
    topic = callback_query.data.replace("help_", "")
    await callback_query.answer()
    await callback_query.edit_message_text(
        f"📘 Help on **{topic.title()}**\n\nℹ️ More details coming soon...\n⚡ Powered by Zain",
        parse_mode="Markdown"
    )

