# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/downloads/instagram.py
# Description: Instagram downloader for reels, posts, and stories
# ============================================

import os
import asyncio
import time
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
    start_time = time.time()
    last_update = {"time": 0, "percent": 0}
    filename = None

    try:
        loader = instaloader.Instaloader(
            dirname_pattern=TEMP_DIR,
            download_videos=True,
            quiet=True
        )

        # Handle cookies for private or logged-in content
        cookie_file = None
        if cookie_data:
            cookie_file = f"{TEMP_DIR}/cookie_{user_id}.txt"
            with open(cookie_file, "w", encoding="utf-8") as f:
                f.write(cookie_data)
            try:
                loader.load_session_from_file("session", cookie_file)
            except Exception:
                pass

        await safe_send(message.reply_text, "📥 Downloading media from Instagram...")

        # Extract shortcode from link (e.g., https://www.instagram.com/reel/XXXXX/)
        shortcode = None
        parts = [p for p in url.strip("/").split("/") if p]
        if len(parts) >= 2:
            shortcode = parts[-1] if parts[-1] else parts[-2]
        if not shortcode:
            return await message.reply("❌ Invalid Instagram link.")

        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=TEMP_DIR)

        # Find downloaded file (video or image)
        for file in os.listdir(TEMP_DIR):
            if file.endswith((".mp4", ".jpg", ".png")):
                filename = os.path.join(TEMP_DIR, file)
                break

        if not filename or not os.path.exists(filename):
            return await message.reply("❌ Failed to locate downloaded file.")

        # Premium size check
        file_size = os.path.getsize(filename)
        if file_size > 500 * 1024 * 1024 and not (await is_premium(user_id) or user_id == OWNER_ID):
            await message.reply("❌ File exceeds 500MB. Premium required for large downloads.")
            os.remove(filename)
            return

        upload_msg = await safe_send(app.send_message, chat_id, "📤 Uploading media to Telegram...")

        # Upload with progress
        with open(filename, "rb") as f:
            if filename.endswith(".mp4"):
                await app.send_video(
                    chat_id,
                    f,
                    caption="✅ Downloaded from Instagram\n⚡ Powered by Zain",
                    progress=progress_callback,
                    progress_args=(
                        0,  # current bytes start placeholder
                        file_size,
                        upload_msg,
                        start_time,
                        1,
                        1,
                        "Uploading",
                        os.path.basename(filename),
                        last_update,
                        f"insta_{user_id}",
                    ),
                )
            else:
                await app.send_photo(
                    chat_id,
                    f,
                    caption="✅ Downloaded from Instagram\n⚡ Powered by Zain",
                )

        # Clean temp files
        cleanup_temp_files()
        await safe_send(upload_msg.edit, "✅ Uploaded successfully!\n⚡ Powered by Zain")

    except Exception as e:
        await safe_send(message.reply_text, f"❌ Error: {str(e)}")
        if filename and os.path.exists(filename):
            os.remove(filename)
