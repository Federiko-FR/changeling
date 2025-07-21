import asyncpg
import asyncio
from decouple import config

async def connection():
    """
    Функция в боте никак не используется, создавал чтобы проверить подключение к бд.
    """
    try:
        conn = await asyncpg.connect(config('PG_LINK'))
        print(" Подключение успешно!")
        await conn.close()
    except Exception as e:
        print(f"Ошибка: {e}")

asyncio.run(connection())