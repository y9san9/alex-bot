import logging
import sys

from app.controller import BotController
from config import SESSION_NAME

sys.path.append("../..")

logging.basicConfig(format="[5s/%(asctime)s] %(name)s: %(message)s",
                    level=logging.INFO)


session = input("Enter session name or Enter to use default: ")

with BotController(session if not session == "" else SESSION_NAME) as bot:
    bot.start()
