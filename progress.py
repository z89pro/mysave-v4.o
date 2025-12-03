# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: progress.py
# Description: Enhanced progress system with stage indicator (Download/Upload)
# ============================================

import math
import time
import asyncio
from datetime import timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

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

def human_readable_time(seconds: float) -> str:
    if seconds <= 0:
        return "-"
    return str(timedelta(seconds=int(seconds)))

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

def make_bar(percent: float) -> str:
    filled = int(percent // 10)
    empty = 10 - filled
    return "▰" * filled + "▱" * empty

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

    stage_icon = "⬇️" if "Download" in stage else "⬆️"
    progress_text = (
        f"{stage_icon} **{stage} Progress ({index}/{total_files})**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 Current File:\n"
        f"{filename}\n\n"
        f"{bar} **{percent:.0f}%**\n\n"
        f"📊 **Processed:** {processed} / {total_h}\n"
        f"⚡ **Speed:** {speed_h}/s | ⏳ **ETA:** {eta_h}\n"
        f"⏰ **Elapsed:** {elapsed}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔄 **Tap to Refresh**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ Powered by Zain | Save Restricted Bot v4"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{task_id}")]]
    )

    await safe_edit(message, progress_text, reply_markup=buttons)
