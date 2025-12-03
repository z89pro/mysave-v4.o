
# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: commands/recover.py
# Description: Resume incomplete batch tasks for users
# ============================================

from utils.safe_send import safe_send
from progress import progress_callback
import asyncio
import time

async def recover_command(client, message, db):
    """
    Resume a previously interrupted batch download or upload.
    Recovers files saved in MongoDB under 'recover' collection.
    """
    user_id = message.from_user.id
    recovery = await db["recover"].find_one({"user_id": user_id})

    if not recovery:
        return await message.reply("ℹ️ No incomplete batch found to recover.")

    files = recovery.get("files", [])
    await message.reply(f"🔁 Recovering batch with {len(files)} files…")

    for index, file in enumerate(files, start=1):
        start = time.time()
        last_update = {"time": 0, "percent": 0}
        task_id = f"recover_{index}"
        msg = await safe_send(client.send_message, user_id, f"Resuming {file['name']}…")

        await progress_callback(
            file["current"],
            file["total"],
            msg,
            start,
            index,
            len(files),
            "Uploading",
            file["name"],
            last_update,
            task_id,
        )

        await asyncio.sleep(15)

    await message.reply("✅ Recovery complete!\n⚡ Powered by Zain")
