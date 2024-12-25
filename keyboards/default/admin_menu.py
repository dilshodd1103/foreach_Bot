from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Foydalanuvchilar soni'),
            KeyboardButton(text='Reklama'),
        ],
        [
            KeyboardButton(text="Kurs qo'shish"),
            KeyboardButton(text="Kursni o'chirish"),
        ],
        [
            KeyboardButton(text="Kursni tahrirlash"),
            KeyboardButton(text="Adminlar"),
        ],
        [
            KeyboardButton(text="Statistika"),
            KeyboardButton(text="Ma'lumotlar")
        ],
        [
            KeyboardButton(text="Alohida xabar")
        ],
        [
            KeyboardButton(text="Menu"),
        ]
    ], resize_keyboard=True
)
