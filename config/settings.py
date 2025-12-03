import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
MONGO_DB = os.getenv("MONGO_DB", "")

# Optional Envs
LOG_GROUP = int(os.getenv("LOG_GROUP", "-100"))
FORCE_SUB = int(os.getenv("FORCE_SUB", "-100"))
VERSION = "4.0-Zain-Fix"
