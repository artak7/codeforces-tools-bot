import asyncio

from app import setup_routes, set_default_commands #, delete_default_commands #, setup_middlewares
from bot import dp, bot
from utils import logger


async def on_startup() -> None:
    # await delete_default_commands() # TODO fix it. does not works
    await set_default_commands()
    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.info("Bot stopped!")


async def main() -> None:
    # await setup_middlewares(dp) # TODO set it up
    await setup_routes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())