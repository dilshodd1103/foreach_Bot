from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


til = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
        ],
    ], resize_keyboard=True, one_time_keyboard=True
)