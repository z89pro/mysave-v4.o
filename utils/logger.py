# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/logger.py
# Description: Colorized console and file logging using Loguru
# ============================================

from loguru import logger
import sys
import os

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Remove default handlers
logger.remove()

# Console log formatting
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{module}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
)

# File logging (rotated weekly)
logger.add(
    f"{LOG_DIR}/bot.log",
    rotation="7 days",
    retention="7 days",
    level="INFO",
    encoding="utf-8",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{line} | {message}",
)

def get_logger():
    """
    Returns a pre-configured global logger instance.
    Example:
        from utils.logger import get_logger
        log = get_logger()
        log.info("Bot started successfully!")
    """
    return logger

