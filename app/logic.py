import json
import os
from typing import Union, List

from telethon import TelegramClient
from telethon.tl.custom import Message
from telethon.tl.types import PeerUser

from utils.file_utils import File

storage = File(os.path.join("storage.json"))
storage.refresh("{}")

copied: Union[Message, None] = None


async def copy(message: Message, client: TelegramClient, args: List[str]):
    global copied

    msg = await message.get_reply_message()
    if msg is None:
        await message.edit("No message replied")
    else:
        await message.delete()
        if len(args) == 0:
            copied = msg
        else:
            await copy_named(msg, client, args[0])


async def copy_named(message: Message, client: TelegramClient, name: str):
    msg: Message = await client.send_message("me", message)
    data = storage.read_object()
    data[name] = msg.id
    storage.write_object(data)


async def paste(message: Message, client: TelegramClient, args: List[str]):
    if len(args) == 0:
        global copied
        if copied is None:
            await message.edit("No message copied")
        else:
            await message.delete()
            await client.send_message(message.to_id, copied, reply_to=message.reply_to_msg_id)
    else:
        await paste_named(message, client, args[0])


async def paste_named(message: Message, client: TelegramClient, name: str):
    data = storage.read_object()
    await message.delete()
    if name in data:
        msg = await client.get_messages("me", min_id=data[name] - 1, max_id=data[name] + 1)
        await client.send_message(message.to_id, msg[0], reply_to=message.reply_to_msg_id)


async def copied_list(message: Message, client: TelegramClient, args: List[str]):
    await message.reply(
        "\n".join(["- " + x[0] for x in storage.read_object().items()])
    )


async def remove(message: Message, client: TelegramClient, args: List[str]):
    global copied
    if len(args) == 0:
        await message.reply("Removed buffer")
        copied = None
    else:
        name = args[0]
        data = storage.read_object()
        if name in data:
            await message.reply(f"Removed {name}")
            del data[name]
            storage.write_object(data)
        else:
            await message.reply(f"Cannot find key {name}")


handlers = {
    ".copy": copy,      ".c": copy,     ".+": copy,
    ".paste": paste,    ".p": paste,    ".=": paste,
    ".remove": remove,  ".r": remove,   ".-": remove,
    ".all": copied_list
}


async def handle_out_message(message: Message, client: TelegramClient):
    args = message.text.split(" ")
    command = args[0]
    await handlers[command](message, client, args[1:]) if command in handlers else None
