from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

async def cookie_command(client, message):
    await message.reply("📥 Send your `cookie.txt` file now.")
    
    try:
        # Requires pyromod
        resp = await client.listen(filters.user(message.from_user.id) & filters.document, timeout=60)
        file = await client.download_media(resp.document)
        with open(file, "r") as f: content = f.read()
        
        c_type = "yt_cookie" if "youtube" in content else "insta_cookie"
        await user_cookies.update_one({"user_id": message.from_user.id}, {"$set": {c_type: content}}, upsert=True)
        await message.reply(f"✅ Saved {c_type}!")
        
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
