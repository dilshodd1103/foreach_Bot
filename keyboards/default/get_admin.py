from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Adminlarni ko'rish"),
            KeyboardButton(text="Admin tayinlash"),
        ],
        [
            KeyboardButton(text="Ortga")
        ],
    ], resize_keyboard=True
)
