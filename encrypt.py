"""
Encryption/Decryption Module - Hide channel links
"""

from cryptography.fernet import Fernet
import os
import json

# Encryption key (generate once and keep it safe)
ENCRYPTION_KEY_FILE = "encryption.key"

def get_or_create_key() -> bytes:
    """Get encryption key or create a new one"""
    if os.path.exists(ENCRYPTION_KEY_FILE):
        with open(ENCRYPTION_KEY_FILE, "rb") as f:
            return f.read()
    else:
        # Generate new key
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, "wb") as f:
            f.write(key)
        print(f"✅ Encryption key created: {ENCRYPTION_KEY_FILE}")
        return key


def encrypt_url(url: str) -> str:
    """Encrypt a URL"""
    try:
        key = get_or_create_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(url.encode())
        return encrypted.decode()
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        return None


def decrypt_url(encrypted_url: str) -> str:
    """Decrypt a URL"""
    try:
        key = get_or_create_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_url.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"❌ Decryption error: {e}")
        return None


def encrypt_batch(urls_dict: dict) -> dict:
    """Encrypt multiple URLs"""
    encrypted = {}
    for name, url in urls_dict.items():
        encrypted[name] = encrypt_url(url)
    return encrypted


def decrypt_batch(encrypted_dict: dict) -> dict:
    """Decrypt multiple URLs"""
    decrypted = {}
    for name, encrypted_url in encrypted_dict.items():
        decrypted[name] = decrypt_url(encrypted_url)
    return decrypted
