from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# CallbackData obyekti yaratish
kurs_callback = CallbackData('kurs', 'id', 'action')

def confirm_delete_buttons(kurs_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Ha", callback_data=kurs_callback.new(id=kurs_id, action='yes')),
        InlineKeyboardButton("Yo'q", callback_data=kurs_callback.new(id=kurs_id, action='no'))
    )
