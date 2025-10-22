from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from data.locales.text import start_text, commands_text 
from app.keyboards import get_menu_keyboard
from ..routes import user_router as router
from bot import bot
from app.commands.default import get_default_commands
from aiogram.types import BotCommandScopeChat
# from bot import _


@router.message(CommandStart())
async def start_handler(message: Message):
    text = start_text #_("Hello {}\n" + start_text).format(html.quote(message.from_user.full_name))
    await message.answer(text, reply_markup=get_menu_keyboard())

    # Ensure correct commands for this chat override any old chat-specific or language-specific commands
    lang = getattr(message.from_user, "language_code", None)
    try:
        await bot.set_my_commands(
            get_default_commands(),
            scope=BotCommandScopeChat(chat_id=message.chat.id),
            language_code=lang if isinstance(lang, str) and len(lang) <= 2 else None,
        )
    except Exception:
        # Fallback without language code
        await bot.set_my_commands(
            get_default_commands(),
            scope=BotCommandScopeChat(chat_id=message.chat.id),
        )


# @router.message(Command('stop'))
# async def stop_handler(message: Message):
#     text = _("Bye {}").format(html.quote(message.from_user.full_name))
#     await message.answer(text)


@router.message(Command('help'))
async def help_handler(message: Message):
    text = commands_text
    await message.answer(text)