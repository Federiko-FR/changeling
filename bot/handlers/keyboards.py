from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="повторный запрос", callback_data="repeat_request"),
            InlineKeyboardButton(text="ссылка на модель", url="https://huggingface.co/deepseek-ai/DeepSeek-R1")
        ]
    ])

def get_reply_keyboard():
    buttons = [
        [KeyboardButton(text="что ты умеешь?")],
        [KeyboardButton(text="повторный запрос")],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return markup