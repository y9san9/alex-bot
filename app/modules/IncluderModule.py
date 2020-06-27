import os
from typing import List

from telethon.tl.custom import Message

from app.Module import module, Module, command
from utils.file_utils import File

try:
    from utils.module_utils import import_modules
except ImportError:
    import_modules = None


imports_file = File("../modules/__init__.py")


@command(".module")
async def module_operation(message: Message, args: List[str]):
    base = f"`{message.text}`:\n"

    if len(args) == 0:
        await message.edit(base + "Select operation to invoke")
        return
    operation = args[0]

    if operation == "add":
        await add_module(base, message, args)
    if operation == "remove":
        await remove(base, message, args)
    if operation == "list":
        await list_modules(base, message, args)


async def add_module(base: str, message: Message, args: List[str]):
    if len(args) < 2 or message.file is None:
        await message.edit(base + "You should use `.module add {module_name}` and attach file with source code")
        return
    name = args[1]
    code_file = message.file.media
    code = await message.client.download_file(code_file)

    file = File(f"../modules/{name}.py")
    if file.exists():
        await message.edit(base + f"Sorry, module file {name}.py already exists")
        return

    file.refresh()
    file.write(code)
    imports_file.append(f"\nfrom app.modules import {name}")
    try:
        exec(f"import app.modules.{name}")
    except Exception as e:
        await remove(base, message, args)
        await message.edit(base + f"Error while importing module: \n`{e}`")
        return

    await import_modules(message.client)
    await message.edit(base + f"Added {name}")


async def remove(base: str, message: Message, args: List[str]):

    if len(args) < 2:
        await message.edit(base + "Provide module filename to remove")
        return
    name = args[1]

    file = File(f"../modules/{name}.py")
    if not file.exists():
        await message.edit(base + f"Cannot find module file {name}.py")
        return

    imports = (x for x in imports_file.read().splitlines() if x != f"from app.modules import {name}")
    imports_file.write("\n".join(imports))
    file.delete()

    await import_modules(message.client)
    await message.edit(base + f"Removed {name}")


async def list_modules(base: str, message: Message, _):
    await message.edit(base + "Installed module files:\n" +
                       "\n".join(f"- {x}" for x in os.listdir("../modules") if not x.startswith("__")))


@module
class Includer(Module):
    @staticmethod
    def help() -> str:
        return "Module includer"
