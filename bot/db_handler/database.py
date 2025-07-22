import asyncpg
from decouple import config

async def create_pool():
    """
    Создает пулл подключений к бд
    :return: Pool
    """
    return await asyncpg.create_pool(config('PG_LINK'))

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