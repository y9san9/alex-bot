from typing import List

from telethon import TelegramClient
from telethon.tl.custom import Message

from app.Module import module, Module, command
from utils.file_utils import File


@module
class CopyPaste(Module):
    def __init__(self):
        self.me = self.storage = self.copied = None

    @staticmethod
    def help() -> str:
        return "Internal CopyPast module for AlexBot\n" \
               "Usage:\n" \
               "- `.copy`, `.c`, `.+` [name] - copy message reply to buffer or storage if " \
               "name specified\n" + \
               "- `.paste`, `.p`, `.=` [name] - paste message from buffer or by name if specified\n" + \
               "- `.remove`, `.r`, `.-` [name] - remove message from buffer or by name if specified\n" + \
               "- `.copied` - prints all saved copies "

    async def install(self, client: TelegramClient):
        self.me = await client.get_me()
        self.storage = File(f"{self.me.id}_storage.json")
        self.storage.refresh("{}")

        @command(".copy", ".c", ".+")
        async def copy(message: Message, args: List[str]):
            await self.copy(message, args)

        @command(".paste", ".p", ".=")
        async def paste(message: Message, args: List[str]):
            await self.paste(message, args)

        @command(".remove", ".r", ".-")
        async def remove(message: Message, args: List[str]):
            await self.remove(message, args)

        @command(".copied")
        async def all_copied(message: Message, _):
            await self.all_copied(message)

    async def copy(self, message: Message, args: List[str]):
        reply = await message.get_reply_message()
        await message.delete()
        if reply is None:
            await message.edit("`.copy`:\nMessage reply is not provided")
            return
        if len(args) == 0:
            self.copied = reply
        else:
            await self.copy_named(reply, args[0])

    async def copy_named(self, reply: Message, name: str):
        msg = await reply.client.send_message("me", reply)
        data = self.storage.read_object()
        data[name] = msg.id
        self.storage.write_object(data)

    async def paste(self, message: Message, args: List[str]):
        await message.delete()
        if len(args) == 0:
            if self.copied is not None:
                await message.client.send_message(message.to_id, self.copied, reply_to=message.reply_to_msg_id)
        else:
            await self.paste_named(message, args[0])

    async def paste_named(self, message: Message, name: str):
        data = self.storage.read_object()
        if name in data:
            msg = await message.client.get_messages("me", min_id=data[name] - 1, max_id=data[name] + 1)
            await message.client.send_message(message.to_id, msg[0], reply_to=message.reply_to_msg_id)

    async def remove(self, message: Message, args: List[str]):
        if len(args) == 0:
            await message.edit("Removed buffer")
            self.copied = None
        else:
            name = args[0]
            data = self.storage.read_object()
            if name in data:
                await message.edit(f"Removed `{name}`")
                del data[name]
                self.storage.write_object(data)
            else:
                await message.edit(f"Cannot find key `{name}`")

    async def all_copied(self, message: Message):
        data = self.storage.read_object()
        str_list = "\n".join(f"- {x[0]}" for x in data.items())
        str_list = "No stored copies yet" if str_list == "" else str_list
        await message.edit("`.all`:\n" + str_list)
