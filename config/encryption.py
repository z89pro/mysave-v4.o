
# ============================================
# ⚡ Save Restricted Content Bot v4 — Zain Edition
# File: config/encryption.py
# Description: AES-GCM encryption and decryption helpers
# ============================================

import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(master_key: str, salt: bytes) -> bytes:
    """
    Derive a 128-bit AES key from a master key using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=390000,
    )
    return kdf.derive(master_key.encode())


def encrypt_text(master_key: str, plaintext: str) -> str:
    """
    Encrypt a plaintext string using AES-GCM with the given master key.
    Returns a base64 string safe for storing in .env files.
    """
    salt = os.urandom(16)
    key = derive_key(master_key, salt)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, plaintext.encode(), None)
    combined = salt + nonce + ciphertext
    return base64.urlsafe_b64encode(combined).decode()


def decrypt_text(master_key: str, encrypted: str) -> str:
    """
    Decrypt a previously encrypted base64 string using AES-GCM.
    """
    raw = base64.urlsafe_b64decode(encrypted)
    salt, nonce, ciphertext = raw[:16], raw[16:28], raw[28:]
    key = derive_key(master_key, salt)
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None).decode()


# Example (run manually to encrypt cookies):
# --------------------------------------------
# from config.encryption import encrypt_text
# MASTER_KEY = "YourMasterKey123"
# enc = encrypt_text(MASTER_KEY, "paste_your_cookie_here")
# print(enc)
#
# Later in settings.py, you’ll decrypt it automatically using decrypt_text().
# ============================================
