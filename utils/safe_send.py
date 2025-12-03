import asyncio
from pyrogram.errors import FloodWait
from loguru import logger

async def safe_send(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        logger.warning(f"FloodWait: Sleeping {e.value}s")
        await asyncio.sleep(e.value + 2)
        return await func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Send Error: {e}")
