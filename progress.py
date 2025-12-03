
import math
import time
import asyncio
from datetime import timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# -------------------------------
# ⚡ Powered by Zain | v4 Engine
# -------------------------------

# Helper to convert bytes to human-readable sizes
def human_readable_bytes(size: int) -> str:
    if not size:
        return "0B"
    power = 1024
    n = 0
    Dic_powerN = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f}{Dic_powerN[n]}B"


# Helper to convert seconds to human-readable time
def human_readable_time(seconds: float) -> str:
    if seconds <= 0:
        return "-"
    return str(timedelta(seconds=int(seconds)))


# FloodWait-safe message editor
async def safe_edit(message, text, reply_markup=None):
    while True:
        try:
            return await message.edit(
                text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
        except FloodWait as e:
            await asyncio.sleep(e.value + 2)
        except Exception:
            break


# Build visual progress bar ▰▱
def make_bar(percent: float) -> str:
    filled = int(percent // 10)
    empty = 10 - filled
    return "▰" * filled + "▱" * empty


# The main progress callback
async def progress_callback(
    current: int,
    total: int,
    message,
    start_time: float,
    index: int,
    total_files: int,
    stage: str,
    filename: str,
    last_update: dict,
    task_id: str,
):
    now = time.time()
    diff = now - start_time
    if diff < 0.5:
        return

    # Update only every 5s or 1% change
    percent = current * 100 / total if total else 0
    if (
        now - last_update.get("time", 0) < 5
        and percent - last_update.get("percent", 0) < 1
    ):
        return

    last_update["time"] = now
    last_update["percent"] = percent

    speed = current / diff if diff > 0 else 0
    eta = (total - current) / speed if speed > 0 else 0

    bar = make_bar(percent)
    processed = human_readable_bytes(current)
    total_h = human_readable_bytes(total)
    speed_h = human_readable_bytes(speed)
    eta_h = human_readable_time(eta)
    elapsed = human_readable_time(diff)

    # Build message text
    progress_text = (
        f"📁 **Batch Progress ({index} / {total_files})**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 Current File:\n"
        f"{filename}\n\n"
        f"📦 **Status:** {stage}...\n\n"
        f"{bar} **{percent:.0f}%**\n\n"
        f"📊 **Processed:** {processed} of {total_h}\n"
        f"⚡ **Speed:** {speed_h}/s | ⏳ **ETA:** {eta_h}\n"
        f"⏰ **Elapsed:** {elapsed}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"             🔄 **Refresh**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ Powered by Zain | Save Restricted Bot v4"
    )

    # Inline refresh button
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{task_id}")]]
    )

    await safe_edit(message, progress_text, reply_markup=buttons)


# -----------------------------
# Example usage in batch.py:
# -----------------------------
"""
from progress import progress_callback

# inside your download or upload loop:
start_time = time.time()
last_update = {"time": 0, "percent": 0}

await progress_callback(
    current_bytes,
    total_bytes,
    progress_message,
    start_time,
    current_index,
    total_files,
    "Downloading",
    filename,
    last_update,
    task_id
)
"""
