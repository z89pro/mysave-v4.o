# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/cleanup.py
# Description: Automatic file cleanup system for startup, post-upload, and exit
# ============================================

import os
import glob
import atexit
import logging

logger = logging.getLogger(__name__)

# File patterns that will be removed on cleanup
PATTERNS = [
    "*.mp4", "*.mkv", "*.webm", "*.part", "*.temp",
    "*.jpg", "*.png", "*.jpeg", "*.mp3", "*.wav"
]

def cleanup_temp_files() -> int:
    """
    Delete all temporary and cached media files matching known patterns.
    Returns the total number of files deleted.
    """
    deleted = 0
    for pattern in PATTERNS:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                deleted += 1
            except Exception as e:
                logger.warning(f"Could not delete {file}: {e}")
    return deleted

def startup_cleanup_banner():
    """
    Run cleanup on startup and print a short banner to confirm action.
    """
    count = cleanup_temp_files()
    banner = (
        f"⚙️ Cleaning temporary files...\n"
        f"✅ {count} old files removed.\n"
        f"🚀 Bot is ready — Powered by Zain\n"
    )
    print(banner)
    return count

def register_exit_cleanup():
    """
    Ensure cleanup runs automatically when the bot exits.
    """
    atexit.register(cleanup_temp_files)
