from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kurs_tahriri = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kurs nomini"),
            KeyboardButton(text="Kurs rasmini ")
        ],
        [
            KeyboardButton(text="Kurs tarifini ")
        ],
        [
            KeyboardButton(text="◀️Ortga")
        ],
    ],
    resize_keyboard=True,
)
