from telethon.tl.types import Message

from app.Module import command, module, Module


@command(".ping")
async def pong(message: Message, _):
    await message.edit("Пинг!")


@module
class PingPong(Module):
    @staticmethod
    def help():
        return "Ping pong module for test if bot is running\n- `.ping` to ping"
