from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from data.locales.text import start_text, commands_text 
from ..routes import user_router as router
# from bot import _


@router.message(CommandStart())
async def start_handler(message: Message):
    text = start_text #_("Hello {}\n" + start_text).format(html.quote(message.from_user.full_name))
    await message.answer(text)


# @router.message(Command('stop'))
# async def stop_handler(message: Message):
#     text = _("Bye {}").format(html.quote(message.from_user.full_name))
#     await message.answer(text)


@router.message(Command('help'))
async def help_handler(message: Message):
    text = commands_text
    await message.answer(text)