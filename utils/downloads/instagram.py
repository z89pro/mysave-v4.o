# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/downloads/instagram.py
# Description: Instagram downloader for reels, posts, and stories
# ============================================

import os
import asyncio
import instaloader
from utils.safe_send import safe_send
from utils.cleanup import cleanup_temp_files
from progress import progress_callback
from config.settings import OWNER_ID
from premium import is_premium

# Temporary directory for Instagram downloads
TEMP_DIR = "insta_downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

# --------------------------------------------
# Instagram Download Function
# --------------------------------------------

async def download_instagram(app, message, url, cookie_data=None):
    """
    Download Instagram reel, post, or story.
    Uploads to Telegram automatically with progress.
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    start_time = asyncio.get_event_loop().time()
    last_update = {"time": 0, "percent": 0}
    filename = None

    try:
        loader = instaloader.Instaloader(dirname_pattern=TEMP_DIR, download_videos=True, quiet=True)
        cookie_file = None

        # If user has cookies, save them temporarily
        if cookie_data:
            cookie_file = f"{TEMP_DIR}/cookie_{user_id}.txt"
            with open(cookie_file, "w", encoding="utf-8") as f:
                f.write(cookie_data)
            loader.load_session_from_file("session", cookie_file)

        await safe_send(message.reply_text, "📥 Downloading from Instagram...")

        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        loader.download_post(post, target=TEMP_DIR)

        # Find downloaded file
        for file in os.listdir(TEMP_DIR):
            if file.endswith((".mp4", ".jpg")):
                filename = os.path.join(TEMP_DIR, file)
                break

        if not filename:
            return await message.reply("❌ Failed to find downloaded file.")

        file_size = os.path.getsize(filename)
        if file_size > 500 * 1024 * 1024 and not (await is_premium(user_id) or user_id == OWNER_ID):
            await message.reply("❌ File too large. Premium users only for >500MB.")
            os.remove(filename)
            return

        upload_msg = await safe_send(app.send_message, chat_id, "📤 Uploading media...")
        with open(filename, "rb") as f:
            if filename.endswith(".mp4"):
                await app.send_video(
                    chat_id,
                    f,
                    caption="✅ Downloaded from Instagram\n⚡ Powered by Zain",
                    progress=progress_callback,
                    progress_args=(upload_msg, start_time, 1, 1, "Uploading", filename, last_update, f"insta_{user_id}"),
                )
            else:
                await app.send_photo(
                    chat_id,
                    f,
                    caption="✅ Downloaded from Instagram\n⚡ Powered
