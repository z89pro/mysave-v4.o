# utils/safe_send.py
import asyncio, logging
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

async def safe_send(func, *args, **kwargs):
    """Safely send/edit messages, automatically handle FloodWait."""
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"[FloodWait] sleeping for {wait_time}s")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logger.error(f"[safe_send] {e}")
            break

