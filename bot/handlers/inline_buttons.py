from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
import logging
from handlers.keyboards import get_inline_keyboard

logger = logging.getLogger(__name__)
inline_router = Router()

@inline_router.callback_query(F.data == "repeat_request")
async def handle_repeat_request(callback: CallbackQuery):
    try:
        await callback.answer()

        logger.info(
            f"Обработка кнопки от {callback.from_user.id}. "
            f"Сообщение: {callback.message.text}"
        )
        await callback.message.edit_text(
            text=f"🔁 Повтор: {callback.message.text}",
            reply_markup=get_inline_keyboard()
        )

    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопки: {e}")
        await callback.answer("Произошла ошибка", show_alert=True)
