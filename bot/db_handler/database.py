from typing import Union
import asyncpg
from decouple import config
from aiogram import Dispatcher
from middleware.db import DBMiddleware

async def create_pool():
    """
    Создает пулл подключений к бд
    :return: Pool
    """
    return await asyncpg.create_pool(
        dsn=f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@db:5432/{config('POSTGRES_DB')}?sslmode=disable"
    )
async def add_message(pool, user_id: int, message_text: str):
    """
    Добавляет сообщение в бд
    :param pool: пулл подключений
    :param user_id: идентификатор пользователя который отправил сообщение
    :param message_text: сообщение пользователя
    """
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO messages (user_id, message)
            VALUES ($1, $2)
        """, user_id, message_text)

async def get_last_messages(pool, user_id: int, limit: int = 5):
    """
    Возвращает из бд 5 последних сообщений пользователя
    :param pool: пулл подключений к бд
    :param user_id: идентификатор пользователя
    :param limit: колличество возвращаемых сообщений
    :return: последние limit сообщений пользователя
    """
    async with pool.acquire() as conn:
        return await conn.fetch("""
            SELECT message, dt
            FROM messages
            WHERE user_id = $1
            ORDER BY dt DESC
            LIMIT $2
        """, user_id, limit)


async def setup_database(dp: Dispatcher):
    try:
        pool = await create_pool()
        dp.update.middleware(DBMiddleware(pool))
    except Exception:
        raise RuntimeError('ошибка подключения к базе данных')
    return pool

async def close_db(db: Union[asyncpg.Pool, asyncpg.Connection]):
    await db.close()