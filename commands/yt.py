from pyrogram import filters
from utils.downloads.youtube import download_youtube
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

async def yt_command(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/yt <link>`")
    
    url = message.command[1]
    user_id = message.from_user.id
    
    # Check for saved cookies
    data = await user_cookies.find_one({"user_id": user_id})
    cookie_file = None
    if data and "yt_cookie" in data:
        cookie_file = f"cookie_{user_id}.txt"
        with open(cookie_file, "w") as f: f.write(data["yt_cookie"])
        
    await download_youtube(client, message, url, cookie_file=cookie_file)

async def yt_callback(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if str(user_id) not in data: return await callback_query.answer("Not yours!")
    
    msg = callback_query.message.reply_to_message
    if not msg: return
    
    url = msg.command[1]
    quality = "audio" if "audio" in data else data.split("_")[1].replace("p", "")
    
    await callback_query.message.edit(f"Downloading {quality}...")
    await download_youtube(client, callback_query.message, url, quality_choice=quality)
