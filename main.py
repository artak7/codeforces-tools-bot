import asyncio
from aiohttp import web

from app import setup_routes, set_default_commands #, delete_default_commands #, setup_middlewares
from bot import dp, bot, app
from utils import logger
from data.configs_reader import WEBHOOK_URL, PORT


async def on_startup() -> None:
    # await delete_default_commands() # TODO fix it. does not works
    await set_default_commands()
    await bot.set_webhook(WEBHOOK_URL)
    logger.info("Bot started!")


async def on_shutdown() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logger.info("Bot stopped!")
    # Redis
    # await dp.storage.close() 
    # await dp.storage.wait_closed() 


def main() -> None:
    # await setup_middlewares(dp) # TODO set it up
    # await 
    setup_routes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if WEBHOOK_URL is None:
        # await
        dp.start_polling(bot)
    else:
        web.run_app(app, host="0.0.0.0", port=PORT)  # Start server


if __name__ == "__main__":
    # asyncio.run(main())
    main()