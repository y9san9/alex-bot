from telethon.events import NewMessage
from telethon.sync import TelegramClient, events

from app.logic import handle_out_message
from config import *


class BotController:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_KEY, API_HASH)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.__exit__(exc_type, exc_val, exc_tb)

    def start(self):
        @self.client.on(NewMessage)
        async def message(event: NewMessage.Event):
            msg = event.message
            if msg.out:
                await handle_out_message(msg, self.client)

        self.client.start()
        self.client.run_until_disconnected()
