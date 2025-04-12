from aiogram.types import BotCommand, BotCommandScopeDefault
from bot import bot #, _, i18n


def get_default_commands(lang: str = "en"):
    commands = [
        BotCommand(command="start", description="start chat"), #_("start chat", locale=lang)),
        BotCommand(command="help", description="help info"), #_("help info", locale=lang)),
        BotCommand(command="load_default_configs", description="load default configs"), #_("load default configs", locale=lang)),
        BotCommand(command="get_configs", description="get configs"), #_("get configs", locale=lang)),
        BotCommand(command="set_configs", description="set configs"), #_("set configs", locale=lang)),
        BotCommand(command="unfreeze_standings", description="unfreeze standings"), #_("unfreeze standings", locale=lang)),
        BotCommand(command="get_new_contestants", description="check new contestants"), #_("check new contestants", locale=lang)),
        BotCommand(command="get_all_contestants", description="get all contestants"), #_("check new contestants", locale=lang)),
        BotCommand(command="set_names", description="set names for anonymous contestants"), #_("check new contestants", locale=lang)),
        # BotCommand(command="/stop", description=_("stop chat", locale=lang)),
        # BotCommand(command="/lang", description=_("change language", locale=lang)),
    ]

    return commands


# async def delete_default_commands():


async def set_default_commands():
    await bot.delete_my_commands(scope=BotCommandScopeDefault()) # Doesnt work!!
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    # for lang in i18n.available_locales:
    #     await bot.set_my_commands(
    #         get_default_commands(lang), scope=BotCommandScopeDefault(), language_code=lang
    #     )
