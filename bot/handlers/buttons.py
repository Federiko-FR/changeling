from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram import Router
import logging

logger = logging.getLogger(__name__)
inline_router = Router()

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="повторный запрос", callback_data="repeat_request"),
        InlineKeyboardButton(text="ссылка на модель", url="https://huggingface.co/deepseek-ai/DeepSeek-R1")
    ]
])


@inline_router.callback_query(lambda c: c.data == "repeat_request")
async def handle_repeat_request(callback: CallbackQuery):
    try:
        await callback.answer()

        logger.info(
            f"Обработка кнопки от {callback.from_user.id}. "
            f"Сообщение: {callback.message.text}"
        )

        await callback.message.edit_text(
            text=f"🔁 Повтор: {callback.message.text}",
            reply_markup=inline_kb
        )

    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопки: {e}")
        await callback.answer("Произошла ошибка", show_alert=True)
