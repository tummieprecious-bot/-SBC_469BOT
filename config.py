import os

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables!")
