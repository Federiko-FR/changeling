from aiogram.types import Message
from aiogram import Router, F
import logging
from handlers.keyboards import get_inline_keyboard

logger = logging.getLogger(__name__)
reply_router = Router()

@reply_router.message(F.data == "повторный запрос")
async def handle_repeat_request(message: Message):
    await message.answer("Чем вам помочь?")
    logger.info('сработал reply обработчик')