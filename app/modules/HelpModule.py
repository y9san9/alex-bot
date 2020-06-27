from typing import List

from telethon.tl.custom import Message

from app.Module import command, handlers, modules


@command(".help", ".h")
async def help_message(message: Message, args: List[str]):
    base = f"`{message.text}`:\n"
    if len(args) == 0:
        await message.edit(base + "Installed modules:\n" + "\n".join([f"- {x.__name__}" for x in modules])
                           + "\nUse `.h {module}` for module help")
    else:
        module = [x for x in modules if x.__name__ == args[0]]
        if len(module) == 0:
            await message.edit(base + f"No module named `{args[0]}`")
        help_text = module[0].help()
        await message.edit(base +
                           (f"No help provided for module `{module.__name__}`" if help_text is None else help_text)
                           )
