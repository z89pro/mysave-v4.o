from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_DB

db = AsyncIOMotorClient(MONGO_DB)["savebot"]
user_cookies = db["user_cookies"]

async def cookie_command(client, message):
    await message.reply("📥 Send your `cookie.txt` file now.", quote=True)
    
    # This requires pyromod to work
    try:
        response = await client.listen(filters.user(message.from_user.id) & filters.document, timeout=60)
    except Exception:
        return await message.reply("⏰ Timeout.")

    doc = response.document
    if not doc.file_name.endswith(".txt"):
        return await message.reply("❌ Must be a .txt file.")

    file_path = await client.download_media(doc)
    with open(file_path, "r", encoding="utf-8") as f:
        cookie_text = f.read()

    detected = "yt" if "youtube.com" in cookie_text else "insta" if "instagram.com" in cookie_text else None
    
    if not detected:
        return await message.reply("❌ Unknown cookie type.")

    user_id = message.from_user.id
    field = "yt_cookie" if detected == "yt" else "insta_cookie"
    
    await user_cookies.update_one(
        {"user_id": user_id}, 
        {"$set": {field: cookie_text}}, 
        upsert=True
    )
    await message.reply(f"✅ Saved {detected} cookie!")
