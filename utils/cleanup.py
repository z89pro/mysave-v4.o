# utils/cleanup.py
import os, glob, atexit, logging

logger = logging.getLogger(__name__)

PATTERNS = [
    "*.mp4", "*.mkv", "*.webm", "*.part", "*.temp",
    "*.jpg", "*.png", "*.jpeg", "*.mp3", "*.wav"
]

def cleanup_temp_files() -> int:
    """Delete all temporary/cached media files."""
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
    count = cleanup_temp_files()
    banner = (
        f"⚙️ Cleaning temporary files...\n"
        f"✅ {count} old files removed.\n"
        f"🚀 Bot is ready — Powered by Zain\n"
    )
    print(banner)
    return count


def register_exit_cleanup():
    """Ensure cleanup runs on exit."""
    atexit.register(cleanup_temp_files)

