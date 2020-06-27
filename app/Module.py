import re

from telethon import TelegramClient
from telethon.tl.patched import Message


modules = []
handlers = {}


def command(*texts: str):
    def decorator(func):
        for text in texts:
            handlers[text] = func
        return func

    return decorator


def module(clazz):
    modules.append(clazz)
    return clazz


async def handle_message(message: Message):
    args = re.split("\\s", message.text)
    cmd = args[0]
    args = args[1:] if len(args) > 1 else []
    if cmd in handlers:
        await handlers[cmd](message, args)


class Module:
    async def install(self, client: TelegramClient):
        pass

    @staticmethod
    def help() -> str:
        pass
