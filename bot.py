from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from data.configs_reader import TELEGRAM_BOT_TOKEN, I18N_DOMAIN, I18N_PATH


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
i18n = I18n(path=I18N_PATH, domain=I18N_DOMAIN)
_ = i18n.gettext



from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web


# 👇 Health check endpoint (required for Render)
async def health_check(request):
    return web.Response(text="Bot is alive!")

app = web.Application()


def setup_webhook_app():
    """Configure webhook handlers"""
    app.add_routes([web.get("/", health_check)])
    webhook_handler = SimpleRequestHandler(dp, bot)
    webhook_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    return app