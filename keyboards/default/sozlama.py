from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sozlama = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="♻️Ismni o'zgartirish"),
            KeyboardButton(text="🔢Raqamni o'zgartirish")
        ],
        [
            KeyboardButton(text="🔄Tilni almashtirish")
        ],
        [
            KeyboardButton(text="◀️Ortga")
        ]
    ], resize_keyboard=True
)
