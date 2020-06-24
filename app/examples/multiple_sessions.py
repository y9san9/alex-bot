import asyncio
from threading import *

from app.controller import BotController
import logging

from config import SESSION_NAME

logging.basicConfig(format='[5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)


def start_new(session_name=SESSION_NAME):
    def start():
        asyncio.set_event_loop(asyncio.new_event_loop())
        with BotController(session_name) as bot:
            bot.start()
    Thread(target=start).start()


# input should be
# +7######### - first number
# +7######### - second number
# 123456 - first number code
# 123456 - second number code
start_new()
start_new("second_session")
