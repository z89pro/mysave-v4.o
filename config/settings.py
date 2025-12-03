# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: config/settings.py
# Description: Environment loader and secure configuration manager
# ============================================

import os
from dotenv import load_dotenv
from config.encryption import decrypt_text

# Load all environment variables from .env file
load_dotenv()

# Master encryption key (used to decrypt cookies or secrets)
MASTER_KEY = os.getenv("MASTER_KEY", "zain_default_master")

# Telegram API and Bot credentials
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Owner and database configuration
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
MONGO_DB = os.getenv("MONGO_DB", "")

# Optional logging and subscription channels
LOG_GROUP = int(os.getenv("LOG_GROUP", "-100"))
FORCE_SUB = int(os.getenv("FORCE_SUB", "-100"))

# Optional encrypted cookies (YouTube / Instagram)
YT_COOKIES = os.getenv("YT_COOKIES_ENC")
INSTA_COOKIES = os.getenv("INSTA_COOKIES_ENC")

# Attempt to decrypt cookies if they are encrypted
if YT_COOKIES:
    try:
        YT_COOKIES = decrypt_text(MASTER_KEY, YT_COOKIES)
    except Exception:
        YT_COOKIES = None

if INSTA_COOKIES:
    try:
        INSTA_COOKIES = decrypt_text(MASTER_KEY, INSTA_COOKIES)
    except Exception:
        INSTA_COOKIES = None

# Optional debug and version info
DEBUG = bool(int(os.getenv("DEBUG", "0")))
VERSION = "4.0-Zain"

# ============================================
# ✅ Example of .env file structure:
# --------------------------------------------
# API_ID=123456
# API_HASH=abcd1234efgh5678
# BOT_TOKEN=123456:ABCDEF
# OWNER_ID=987654321
# MONGO_DB=mongodb+srv://user:pass@cluster
# MASTER_KEY=MySuperSecretKey
# LOG_GROUP=-100123456789
# FORCE_SUB=-100987654321
# DEBUG=0
# ============================================

