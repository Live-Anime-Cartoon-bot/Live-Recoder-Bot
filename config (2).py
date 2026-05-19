from os import environ

API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

AUTH_USERS = list(map(int, environ.get("AUTH_USERS", "12345678 87654321").split()))

OWNER_ID = list(map(int, environ.get("OWNER_IDS", "").split()))

DOWNLOAD_DIRECTORY = environ.get("DOWNLOAD_DIRECTORY", "./downloads")

DEFAULT_METADATA = environ.get("DEFAULT_METADATA", "")

DEFAULT_FILENAME = environ.get("DEFAULT_FILENAME", "Toonix")

TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
