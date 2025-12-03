# ============================================
# ⚡ Save Restricted Content Bot v4 — Powered by Zain
# File: config/settings.py
# Description: Secure environment loader with fallback cookie support
# ============================================

import os
from dotenv import load_dotenv
from config.encryption import decrypt_text

load_dotenv()

MASTER_KEY = os.getenv("MASTER_KEY", "zain_default_master")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
MONGO_DB = os.getenv("MONGO_DB", "")

LOG_GROUP = int(os.getenv("LOG_GROUP", "-100"))
FORCE_SUB = int(os.getenv("FORCE_SUB", "-100"))

YT_COOKIES = os.getenv("YT_COOKIES_ENC")
INSTA_COOKIES = os.getenv("INSTA_COOKIES_ENC")

# Optional default cookies (used if user-specific cookies not found)
YT_DEFAULT_COOKIE = os.getenv("YT_DEFAULT_COOKIE", None)
INSTA_DEFAULT_COOKIE = os.getenv("INSTA_DEFAULT_COOKIE", None)

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

DEBUG = bool(int(os.getenv("DEBUG", "0")))
VERSION = "4.0-Zain"
