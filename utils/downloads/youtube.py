# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/downloads/youtube.py
# Description: YouTube downloader with quality/audio selector and progress tracking
# ============================================

import os
import asyncio
import time
import yt_dlp
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.safe_send import safe_send
from utils.cleanup import cleanup_temp_files
from progress import progress_callback
from config.settings import OWNER_ID
from premium import is_premium

# Folder to temporarily store downloads
TEMP_DIR = "downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

# --------------------------------------------
# Helper: yt-dlp options builder
# --------------------------------------------

def build_yt_opts(format_id, cookie_file):
    """Return yt-dlp options for the selected format."""
    opts = {
        "outtmpl": f"{TEMP_DIR}/%(title)s.%(ext)s",
        "quiet": True,
        "progress_hooks": [],
        "noplaylist": True,
        "geo_bypass": True,
        "writethumbnail": False,
        "cookiefile": cookie_file if cookie_file else None,
        "format": format_id,
    }
    return opts

# --------------------------------------------
# Helper: get available formats
# --------------------------------------------

async def get_formats(url, cookie_file=None):
    """Fetch available YouTube formats (video qualities)."""
    ydl_opts = {"quiet": True, "cookiefile": cookie_file}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") != "none" and f.get("acodec") != "none":
                res = f.get("format_note", "unknown")
                fmt_id = f.get("format_id")
                size = f.get("filesize") or 0
                if "video" in f.get("format", ""):
                    formats.append((res, fmt_id, size))
        return info.get("title", "video"), formats

# --------------------------------------------
# Download function
# --------------------------------------------

async def download_youtube(app, message, url, quality_choice=None, cookie_file=None):
    """
    Download a YouTube video or audio based on user selection.
    Shows progress and uploads to Telegram after completion.
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    title, formats = await get_formats(url, cookie_file)
    
    if not quality_choice:
        # Create inline quality selection buttons dynamically
        quality_buttons = [
            [InlineKeyboardButton(f"{res}p", callback_data=f"yt_{res}_{user_id}")]
            for res, fmt_id, size in formats if "p" in res
        ]
        audio_button = [InlineKeyboardButton("🎵 Audio Only", callback_data=f"yt_audio_{user_id}")]
        quality_buttons.append(audio_button)
        await safe_send(message.reply_text,
            f"🎬 **{title}**\n\nSelect download quality:",
            reply_markup=InlineKeyboardMarkup(quality_buttons),
        )
        return

    # Download selected quality/audio
    await safe_send(message.reply_text, f"📥 Downloading **{title}** in {quality_choice}...")
    start_time = time.time()
    last_update = {"time": 0, "percent": 0}
    temp_file = None

    try:
        format_id = quality_choice if quality_choice != "audio" else "bestaudio"
        ydl_opts = build_yt_opts(format_id, cookie_file)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_file = ydl.prepare_filename(info)

        # Auto-upload to Telegram
        file_size = os.path.getsize(temp_file)
        if file_size > 500 * 1024 * 1024 and not (await is_premium(user_id) or user_id == OWNER_ID):
            await message.reply("❌ File too large. Upgrade to premium to download >500MB.")
            os.remove(temp_file)
            return

        upload_msg = await safe_send(app.send_message, chat_id, f"📤 Uploading **{title}**...")
        with open(temp_file, "rb") as f:
            await app.send_video(
                chat_id,
                f,
                caption=f"✅ **{title}**\n⚡ Powered by Zain",
                progress=progress_callback,
                progress_args=(upload_msg, start_time, 1, 1, "Uploading", title, last_update, f"ytup_{user_id}"),
            )

        cleanup_temp_files()
        await safe_send(upload_msg.edit, f"✅ Uploaded successfully!\n⚡ Powered by Zain")

    except Exception as e:
        await safe_send(message.reply_text, f"❌ Error: {str(e)}")
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
