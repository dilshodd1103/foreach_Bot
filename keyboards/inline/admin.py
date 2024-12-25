from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def adminlar(listt, page=1):
    kurs = InlineKeyboardMarkup(row_width=2)

    start_index = (page - 1) * 50
    end_index = start_index + 50
    page_users = listt[start_index:end_index]

    for kurs1 in page_users:
        kurs.insert(InlineKeyboardButton(text=kurs1[1], callback_data=kurs1[0]))

    if page > 1:
        kurs.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"page_{page - 1}"))

    if end_index < len(listt):
        kurs.insert(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"page_{page + 1}"))
    else:
        kurs.insert(InlineKeyboardButton(text="🔙Ortga", callback_data="back1"))

    return kurs

