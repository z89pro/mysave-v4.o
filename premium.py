# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: premium.py
# Description: Premium user management and expiry notification system
# ============================================

import datetime
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB, OWNER_ID

# Initialize MongoDB
client = AsyncIOMotorClient(MONGO_DB)
db = client["savebot"]
premium_users = db["premium_users"]

# --------------------------------------------
# Add, remove, check premium users
# --------------------------------------------

async def add_premium(user_id: int, days: int):
    """
    Add or extend premium access for a user for given number of days.
    """
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    await premium_users.update_one(
        {"user_id": user_id},
        {"$set": {"expireAt": expire}},
        upsert=True,
    )
    return expire


async def remove_premium(user_id: int):
    """
    Remove a user from the premium database.
    """
    await premium_users.delete_one({"user_id": user_id})


async def get_premium(user_id: int):
    """
    Get premium details for a specific user.
    """
    return await premium_users.find_one({"user_id": user_id})


async def is_premium(user_id: int) -> bool:
    """
    Check whether a user currently has active premium access.
    """
    data = await get_premium(user_id)
    if not data:
        return False
    if data.get("expireAt") < datetime.datetime.utcnow():
        await remove_premium(user_id)
        return False
    return True


# --------------------------------------------
# Background expiry notifier
# --------------------------------------------

async def premium_expiry_checker(app):
    """
    Notify users when their premium plan is about to expire.
    Runs every 24 hours.
    """
    while True:
        now = datetime.datetime.utcnow()
        soon = now + datetime.timedelta(days=1)
        async for user in premium_users.find({"expireAt": {"$lt": soon, "$gt": now}}):
            try:
                await app.send_message(
                    user["user_id"],
                    "⚠️ **Your premium plan expires within 24 hours.**\n"
                    "Renew soon to keep full access.\n\n⚡ Powered by Zain",
                )
            except Exception:
                pass
        await asyncio.sleep(86400)  # Run once per day

