from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_delete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilarni o'chirish"),
            KeyboardButton(text="Ortga")
        ],
    ],
    resize_keyboard=True,
)
