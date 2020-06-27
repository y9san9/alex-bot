import importlib
import os
import sys

from telethon import TelegramClient

from app import Module
# noinspection PyUnresolvedReferences
from app import modules


async def import_modules(client: TelegramClient):
    Module.modules = []
    Module.handlers = {}

    for file in os.listdir("../modules/"):
        module_name = f"app.modules.{file.replace('.py', '')}"
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

    for module in Module.modules:
        await module().install(client)
