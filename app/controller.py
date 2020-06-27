from telethon.events import NewMessage
from telethon.sync import TelegramClient

from config import SESSION_NAME, API_KEY, API_HASH
from app.Module import handle_message, modules
from utils.module_utils import import_modules


class BotController:
    def __init__(self, session_name=SESSION_NAME):
        self.client = TelegramClient(session_name, API_KEY, API_HASH)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.__exit__(exc_type, exc_val, exc_tb)

    def start(self):
        self.client.loop.run_until_complete(import_modules(self.client))

        @self.client.on(NewMessage(outgoing=True))
        async def message(event: NewMessage.Event):
            await handle_message(event.message)

        self.client.start()
        self.client.run_until_disconnected()
