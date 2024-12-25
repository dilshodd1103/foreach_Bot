from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📚Bizning kurslarimiz')
        ],
        [
            KeyboardButton(text='📍Manzilimiz'),
        ],
        [
            KeyboardButton(text="🔗Biz bilan bog'lanish"),
            KeyboardButton(text="🛠Sozlamalar")
        ]
    ], resize_keyboard=True
)
