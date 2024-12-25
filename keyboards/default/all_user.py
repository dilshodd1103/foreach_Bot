from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

all_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilarni ko'rish")
        ],
        [
            KeyboardButton(text="◀️Ortga")
        ],
    ],
    resize_keyboard=True,
)
