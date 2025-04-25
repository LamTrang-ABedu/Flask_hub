from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.functions.messages import GetHistoryRequest
import os

SESSION_NAME = "telegram_session"
API_ID = int(os.getenv("TELEGRAM_API_ID", "123456"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "your_api_hash")

def create_client():
    return TelegramClient(SESSION_NAME, API_ID, API_HASH)

def fetch_telegram_media(group_username, limit=20):
    client = create_client()
    client.start()
    media_items = []
    try:
        entity = client.get_entity(group_username)
        history = client(GetHistoryRequest(
            peer=entity, limit=limit, offset_date=None, offset_id=0,
            max_id=0, min_id=0, add_offset=0, hash=0
        ))
        for msg in history.messages:
            if isinstance(msg.media, MessageMediaPhoto):
                media_items.append({"type": "photo", "caption": msg.message, "file_id": msg.id})
            elif isinstance(msg.media, MessageMediaDocument):
                if hasattr(msg.media.document, "mime_type") and "video" in msg.media.document.mime_type:
                    media_items.append({"type": "video", "caption": msg.message, "file_id": msg.id})
    finally:
        client.disconnect()
    return media_items
