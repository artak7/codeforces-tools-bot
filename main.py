import aiogram
import aiohttp
print("Preloaded dependencies")
import asyncio
from aiohttp import web
import signal

from app import setup_routes, set_default_commands #, delete_default_commands #, setup_middlewares
from bot import dp, bot, setup_webhook_app
from utils import logger
from data.configs_reader import WEBHOOK_URL, PORT


async def on_startup() -> None:
    # await delete_default_commands() # TODO fix it. does not works
    await set_default_commands()
    method = 'Long polling'
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        method = 'Webhook'
    logger.info(f'Bot started with {method}')


async def on_shutdown() -> None:
    if WEBHOOK_URL:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()
    logger.info("Bot stopped!")
    # Redis
    # await dp.storage.close() 
    # await dp.storage.wait_closed() 


async def start_webhook():
    # Setup signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    # await setup_middlewares(dp) # TODO set it up
    await setup_routes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    app = setup_webhook_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()
    
    logger.info(f"Server started on port {PORT}")
    try:
        while True:
            await asyncio.sleep(3600)  # Keep alive
    except asyncio.CancelledError:
        logger.info("Received shutdown signal")
    finally:
        await site.stop()
        await runner.cleanup()


async def shutdown():
    logger.info("Initiating graceful shutdown...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


async def start_polling():
    # await setup_middlewares(dp) # TODO set it up
    await setup_routes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        if WEBHOOK_URL:
            asyncio.run(start_webhook())
        else:
            asyncio.run(start_polling())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
