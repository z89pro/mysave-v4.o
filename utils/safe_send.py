# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: utils/safe_send.py
# Description: FloodWait-safe message sender and editor wrapper
# ============================================

import asyncio
import logging
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

async def safe_send(func, *args, **kwargs):
    """
    Safely send or edit Telegram messages.
    Automatically handles FloodWait by pausing and retrying.
    
    Example usage:
        await safe_send(client.send_message, chat_id, "Processing...")
        await safe_send(message.edit, "✅ Done")
    """
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"[FloodWait] Sleeping for {wait_time}s...")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logger.error(f"[safe_send] Error: {e}")
            break
