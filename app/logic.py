import os
from typing import Union, List, Dict
from telethon.tl.custom import Message
from telethon.tl.types import PeerUser, User

from utils.file_utils import File


def storage(session: str) -> File:
    f = File(os.path.join(f"{session}_storage.json"))
    f.refresh("{}")
    return f


copied: Dict[str, Message] = {}


async def copy(session: str, message: Message, args: List[str]):
    global copied

    msg = await message.get_reply_message()
    if msg is None:
        await message.edit("No message replied")
    else:
        await message.delete()
        if len(args) == 0:
            copied[session] = msg
        else:
            await copy_named(session, msg, args[0])


async def copy_named(session: str, message: Message, name: str):
    msg: Message = await message.client.send_message("me", message)
    data = storage(session).read_object()
    data[name] = msg.id
    storage(session).write_object(data)


async def paste(session: str, message: Message, args: List[str]):
    if len(args) == 0:
        global copied
        if session in copied:
            await message.delete()
            await message.client.send_message(message.to_id, copied[session], reply_to=message.reply_to_msg_id)
        else:
            await message.edit("No message copied")
    else:
        await paste_named(session, message, args[0])


async def paste_named(session: str, message: Message, name: str):
    data = storage(session).read_object()
    await message.delete()
    if name in data:
        msg = await message.client.get_messages("me", min_id=data[name] - 1, max_id=data[name] + 1)
        await message.client.send_message(message.to_id, msg[0], reply_to=message.reply_to_msg_id)


async def copied_list(session: str, message: Message, _: List[str]):
    await message.reply(
        "\n".join(["- " + x[0] for x in storage(session).read_object().items()])
    )


async def remove(session: str, message: Message, args: List[str]):
    global copied
    if len(args) == 0:
        await message.edit("Removed buffer")
        del copied[session]
    else:
        name = args[0]
        data = storage(session).read_object()
        if name in data:
            await message.edit(f"Removed {name}")
            del data[name]
            storage(session).write_object(data)
        else:
            await message.edit(f"Cannot find key {name}")


async def user(session: str, message: Message, args: List[str]):
    if len(args) == 0 or not args[0].isnumeric():
        await message.edit("Id not selected")
    else:
        try:
            user_info = await message.client.get_entity(PeerUser(int(args[0])))
            await message.edit(f"[User](tg://user?id={args[0]}):"
                               f"\n`{user_info.to_json(indent=4)}`")
        except ValueError:
            await message.edit("User not found")


async def dump(session: str, message: Message, args: List[str]):
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


async def handle_out_message(session: str, message: Message):
    args = message.text.split(" ")
    command = args[0]
    await handlers[command](session, message, args[1:]) if command in handlers else None
