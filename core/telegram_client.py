from telethon import TelegramClient
from config import settings

client = TelegramClient(
    'gemini_userbot_session',
    settings.API_ID,
    settings.API_HASH
)

def get_telegram_client() -> TelegramClient:
    return client
