import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from middleware.db import DBMiddleware
from db_handler.database import create_pool


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

async def setup_database():
    try:
        pool = await create_pool()
        dp.update.middleware(DBMiddleware(pool))
    except Exception:
        raise RuntimeError('ошибка подключения к базе данных')
    return pool