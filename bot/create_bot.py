import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from aiohttp import web
from middleware.bot import State
from db_handler.database import close_db, setup_database
from handlers.start import start_router, set_bot_commands
from handlers.buttons import inline_router

logger = logging.getLogger(__name__)

def main():
    """
    Основная функция запуска бота и бд.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    loop = asyncio.get_event_loop()
    app = web.Application(logger=logger)
    state = State(
        app=app,
        bot=bot,
        dp=dp,
        loop=loop
    )
    app.state = state
    bot.state = state
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path="/webhook/")
    setup_application(app, dp, bot=bot)
    web.run_app(
        app,
        host="0.0.0.0",
        port=8081,
        loop=loop
    )

async def on_startup(app: web.Application):
    state: State = app.state
    if not state:
        raise RuntimeError
    state.db_pool = await setup_database(state.dp)
    logger.info("PostgreSQL CONNECTED")

    await set_bot_commands(state.bot)

    state.dp.include_router(start_router)
    state.dp.include_router(inline_router)
    logger.info("Routes LOADED")

    await state.bot.set_webhook(
        url=f"{config('TUNA_URL')}/webhook/",
        drop_pending_updates=True
    )
    logger.info("Bot started")
    logger.info(await state.bot.get_my_commands())
    logger.info("Registered routers: %s", state.dp.sub_routers)


async def on_shutdown(app: web.Application):
    state: State = app.state
    if not state:
        return
    await state.bot.delete_webhook()
    logger.info("WebHook CLOSED")
    await close_db(state.db_pool)
    logger.info("PostgreSQL CLOSED")

