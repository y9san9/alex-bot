import logging

from app.controller import BotController

logging.basicConfig(format="[5s/%(asctime)s] %(name)s: %(message)s",
                    level=logging.INFO)


with BotController() as bot:
    bot.start()
