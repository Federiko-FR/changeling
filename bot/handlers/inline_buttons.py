from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
import logging
from handlers.keyboards import get_inline_keyboard
from handlers.start import deep_seek_api
from db_handler.database import get_last_messages

logger = logging.getLogger(__name__)
inline_router = Router()

@inline_router.callback_query(F.data == "repeat_request")
async def handle_repeat_request(callback: CallbackQuery, pool, bot: Bot):
    try:
        await callback.answer()

        logger.info(
            f"Обработка кнопки от {callback.from_user.id}. "
            f"Сообщение: {callback.message.text}"
        )
        last_message= await get_last_messages(pool, callback.from_user.id, 1)
        normal_last_message = list(last_message)
        logger.info(normal_last_message[0][0])
        await deep_seek_api(normal_last_message[0][0], callback.message.chat.id, bot)

    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопки: {e}")
        await callback.answer("Произошла ошибка", show_alert=True)
