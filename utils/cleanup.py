# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/cleanup.py
# Description: Automatic cleanup system for downloaded files and temp folders
# ============================================

import os
import glob
import shutil
import atexit
import logging

logger = logging.getLogger(__name__)

# File patterns that will be removed on cleanup
PATTERNS = [
    "*.mp4", "*.mkv", "*.webm", "*.part", "*.temp",
    "*.jpg", "*.png", "*.jpeg", "*.mp3", "*.wav",
]

# Temporary directories for YouTube and Instagram
TEMP_FOLDERS = [
    "downloads",
    "insta_downloads",
]

def cleanup_temp_files() -> int:
    """
    Delete temporary and cached media files matching known patterns.
    Also removes content from downloads/ and insta_downloads directories.
    Returns total number of files deleted.
    """
    deleted = 0
    for pattern in PATTERNS:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                deleted += 1
            except Exception as e:
                logger.warning(f"Could not delete {file}: {e}")

    for folder in TEMP_FOLDERS:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                path = os.path.join(folder, file)
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                        deleted += 1
                    elif os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                        deleted += 1
                except Exception as e:
                    logger.warning(f"Failed to clean {path}: {e}")
    return deleted

def startup_cleanup_banner():
    """Run cleanup on startup and print a short banner."""
    count = cleanup_temp_files()
    banner = (
        f"⚙️ Cleaning temporary files...\n"
        f"✅ {count} old files removed.\n"
        f"🚀 Bot is ready — Powered by Zain\n"
    )
    print(banner)
    return count

def register_exit_cleanup():
    """Ensure cleanup runs automatically on exit."""
    atexit.register(cleanup_temp_files)
