from os import environ

API_ID = int(environ.get("API_ID", "29481626"))
API_HASH = environ.get("API_HASH", "4892185769903521077c4cea97808b8c")
BOT_TOKEN = environ.get("BOT_TOKEN", "8619959255:AAGEkg8chHCcgaRkFVYcJ10mrFqyyNq2Y9o")

# ðŸ‘¥ Authorized Users - Bot will work only with these users
AUTH_USERS = list(map(int, environ.get("AUTH_USERS", "5856009289 87654321").split()))

# ðŸ‘‘ Owner/Admin ID - Multiple owners supported
OWNER_ID = list(map(int, environ.get("OWNER_IDS", "5856009289").split()))

DOWNLOAD_DIRECTORY = environ.get("DOWNLOAD_DIRECTORY", "./downloads")

DEFAULT_METADATA = environ.get("DEFAULT_METADATA", "")

DEFAULT_FILENAME = environ.get("DEFAULT_FILENAME", "LS")

TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
