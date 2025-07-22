from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from db_handler.database import add_message, get_last_messages

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    хэндлер /start отправляет приветсвенное сообщение пользователю
    """
    await message.answer('Приветственное сообщение!')

@start_router.message(Command('history'))
async def show_history(message: Message, pool):
    """
    хэндлер /history
    :return: последние 5 сообщений пользователя, если таких нет, то сообщает об этом
    """
    messages = await get_last_messages(pool, message.from_user.id)
    if not messages:
        return await message.answer("У вас пока нет истории сообщений")

    response = "Последние 5 сообщений:\n\n" + "\n".join(
        f"{i + 1}. {msg['message']} ({msg['dt'].strftime('%d-%m-%Y %H:%M')})"
        for i, msg in enumerate(messages)
    )
    await message.answer(response)

@start_router.message()
async def save_message(message: Message, pool):
    """
    Данный хэндлер записывает все сообщений пользователя кроме /start и /history в бд
    """
    await add_message(pool, message.from_user.id, message.text)

