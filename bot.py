from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n

from data.configs_reader import TELEGRAM_BOT_TOKEN, I18N_DOMAIN, I18N_PATH

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
i18n = I18n(path=I18N_PATH, domain=I18N_DOMAIN)
_ = i18n.gettext