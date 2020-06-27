import os
import sys
from typing import List

from telethon.tl.custom import Message

from app.Module import command, module, Module


@command(".dump")
async def dump(message: Message, _):
    reply = await message.get_reply_message()
    await message.edit(f"`.dump`:\n{reply.to_json(indent=4)}")


@command(".py")
async def py(message: Message, args: List[str]):
    default_out = sys.stdout
    sys.stdout = open("")
    result = exec(" ".join(args))
    sys.stdout = default_out

    await message.edit(f"`.py`:\n{result}")


@command(".run")
async def run(message: Message, _):
    await message.edit(message.text + "\n" + str(os.system(" ".join(message.text.split(" ")[1:]))))


@module
class Debug(Module):
    @staticmethod
    def help() -> str:
        return "Debug module:\n" \
               "- `.dump` with message reply to dump it\n" \
               "- `.py {code}` - execute python code\n" \
               "- `.run {code}` - execute os code\n"
