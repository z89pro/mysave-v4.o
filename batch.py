# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: batch.py
# Description: Batch processing handler with progress tracking, cleanup, and cooldown delay
# ============================================

import asyncio
import os
import time
import uuid
from progress import progress_callback
from utils.safe_send import safe_send
from utils.cleanup import cleanup_temp_files

# --------------------------------------------
# Batch Processor
# --------------------------------------------

async def process_batch(app, files, chat_id):
    """
    Process a batch of files sequentially with cooldown delay.
    Each file is uploaded with progress tracking and cleanup.
    """
    total_files = len(files)
    for index, file_path in enumerate(files, start=1):
        filename = os.path.basename(file_path)
        start_time = time.time()
        last_update = {"time": 0, "percent": 0}
        task_id = str(uuid.uuid4())

        # Send initial status message
        progress_msg = await safe_send(app.send_message, chat_id, f"Starting {filename}...")

        # Simulated upload (replace this with actual upload/download logic)
        total = os.path.getsize(file_path)
        current = 0
        chunk = total // 20 or 1

        while current < total:
            current += chunk
            if current > total:
                current = total
            await progress_callback(
                current,
                total,
                progress_msg,
                start_time,
                index,
                total_files,
                "Uploading",
                filename,
                last_update,
                task_id,
            )
            await asyncio.sleep(1)

        await safe_send(progress_msg.edit, f"✅ Uploaded {filename}")
        cleanup_temp_files()

        # Cooldown delay between tasks (FloodWait protection)
        delay = 15
        if total_files > 50:
            delay += 5
        if total_files > 100:
            delay += 10

        await safe_send(app.send_message, chat_id, f"🕒 Waiting {delay}s before next task...")
        await asyncio.sleep(delay)

    await safe_send(app.send_message, chat_id, "✅ Batch processing completed!\n⚡ Powered by Zain")
