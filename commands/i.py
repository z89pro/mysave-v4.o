from utils.downloads.instagram import download_instagram
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

async def insta_command(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/i <link>`")

    url = message.command[1]
    user_id = message.from_user.id

    user = await user_cookies.find_one({"user_id": user_id})
    insta_cookie = user.get("insta_cookie") if user else None

    await download_instagram(client, message, url, cookie_data=insta_cookie)
