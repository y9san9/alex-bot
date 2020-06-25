from telethon.events import NewMessage
from telethon.sync import TelegramClient

from app.logic import handle_out_message
from config import SESSION_NAME, API_KEY, API_HASH


class BotController:
    def __init__(self, session_name=SESSION_NAME):
        self.client = TelegramClient(session_name, API_KEY, API_HASH)
        self.session = session_name

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.__exit__(exc_type, exc_val, exc_tb)

    def start(self):
        @self.client.on(NewMessage(outgoing=True))
        async def message(event: NewMessage.Event):
            await handle_out_message(self.session, event.message)

        self.client.start()
        self.client.run_until_disconnected()
