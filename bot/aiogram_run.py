import asyncio
from create_bot import bot, dp, setup_database
from handlers.start import start_router

async def main():
    """
    Основная функция запуска бота и бд.
    """
    await setup_database()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())