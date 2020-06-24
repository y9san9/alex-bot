import json
import os
from pprint import PrettyPrinter
from typing import Union, List

from telethon import TelegramClient
from telethon.tl import TLObject
from telethon.tl.custom import Message
from telethon.tl.types import PeerUser, User

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
        await message.edit("Removed buffer")
        copied = None
    else:
        name = args[0]
        data = storage.read_object()
        if name in data:
            await message.edit(f"Removed {name}")
            del data[name]
            storage.write_object(data)
        else:
            await message.edit(f"Cannot find key {name}")


async def user(message: Message, client: TelegramClient, args: List[str]):
    if len(args) == 0 or not args[0].isnumeric():
        await message.edit("Id not selected")
    else:
        try:
            user_info = await client.get_entity(PeerUser(int(args[0])))
            await message.edit(f"[User](tg://user?id={args[0]}):"
                               f"\n`{user_info.to_json(indent=4)}`")
        except ValueError:
            await message.edit("User not found")


async def dump(message: Message, client: TelegramClient, args: List[str]):
    reply = await message.get_reply_message()
    await message.edit(f"`{reply.to_json(indent=4)}`")


handlers = {
    ".copy": copy,      ".c": copy,     ".+": copy,
    ".paste": paste,    ".p": paste,    ".=": paste,
    ".remove": remove,  ".r": remove,   ".-": remove,
    ".all": copied_list,
    ".user": user,
    ".dump": dump
}


async def handle_out_message(message: Message, client: TelegramClient):
    args = message.text.split(" ")
    command = args[0]
    await handlers[command](message, client, args[1:]) if command in handlers else None
