from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from data.configs_reader import TELEGRAM_BOT_TOKEN, I18N_DOMAIN, I18N_PATH, RENDER_URL

from aiohttp import web, ClientSession
import asyncio


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
i18n = I18n(path=I18N_PATH, domain=I18N_DOMAIN)
_ = i18n.gettext

app = web.Application()


# 👇 Health check endpoint (required for Render)
async def health_check(request):
    return web.Response(text="OK", content_type="text/plain", status=200)


async def ping_server():
    async with ClientSession() as session:
        while True:
            try:
                async with session.get(f"{RENDER_URL}/") as resp:
                    print(f"Pinged server - Status: {resp.status}")
            except Exception as e:
                print(f"Ping failed: {e}")
            await asyncio.sleep(45)  # Ping every 45 seconds


async def start_background_tasks(app):
    app['keepalive'] = asyncio.create_task(ping_server())


# async def cleanup_background_tasks(app):
#     app['keepalive'].cancel()
#     await app['keepalive']


def setup_webhook_app():
    """Configure webhook handlers"""
    app.add_routes([web.get("/", health_check)])
    app.on_startup.append(start_background_tasks)
    # app.on_cleanup.append(cleanup_background_tasks)
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    webhook_handler = SimpleRequestHandler(dp, bot)
    webhook_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    return app