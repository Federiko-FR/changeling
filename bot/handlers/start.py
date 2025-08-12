from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from db_handler.database import add_message, get_last_messages
from handlers.keyboards import get_inline_keyboard, get_reply_keyboard
import aiohttp
import asyncio
from decouple import config
from aiogram.utils.text_decorations import html_decoration as hd
import re
from html import unescape
import logging

start_router = Router()
logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="history", description="Показать историю сообщений")
    ]
    await bot.set_my_commands(commands)
    logger.info("Команды бота обновлены")

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    хэндлер /start отправляет приветсвенное сообщение пользователю
    """
    await message.answer(text=f'Привет, {str(message.from_user.first_name)}!',reply_markup=get_reply_keyboard())

@start_router.message(Command("history"))
async def cmd_history(message: Message, pool):
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


@start_router.message(F.data != "повторный запрос")
async def save_message(message: Message,bot: Bot, pool):
    """
    Обрабатывает сообщения пользователя:
    1. Пропускает команды /start и /history
    2. Отправляет текст в Hugging Face API
    3. Сохраняет сообщение в БД
    4. Отправляет ответ пользователю
    """
    logger.info('сработал start')
    try:
        await deep_seek_api(message, bot)
    finally:
        await add_message(pool, message.from_user.id, message.text)



async def deep_seek_api(message: Message, bot: Bot):
    user_text = message.text
    headers = {"Authorization": f"Bearer {config('HUGGINGFACE_API_TOKEN')}",
        "Content-Type": "application/json"}
    api_url = config('HUGGINGFACE_API_URL')
    payload = {
        "messages": [{"role": "user", "content": user_text}],
        "model": "deepseek-ai/DeepSeek-R1:novita"
    }
    sent_message = await message.answer('погоди, я думаю!')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=100)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) > 0:
                        raw_text = unescape(data["choices"][0]["message"]["content"])
                        ai_response = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL)
                        ai_response = re.sub(r'\n\s*\n', '\n\n', ai_response).strip()
                    else:
                        ai_response = str(data)
                    safe_response = hd.quote(ai_response)
                    await bot.delete_message(message.chat.id, sent_message.message_id)
                    await message.answer(safe_response, reply_markup=get_inline_keyboard(), parse_mode=None)
                else:
                    error = await response.text()
                    await message.answer(f"Ошибка API (код {response.status}): {error[:500]}...")

    except asyncio.TimeoutError:
        await message.answer("Превышено время ожидания ответа от модели")
    except aiohttp.ClientError as e:
        await message.answer(f"Ошибка соединения: {str(e)}")
    except Exception as e:
        await message.answer(f"Неожиданная ошибка: {str(e)}")