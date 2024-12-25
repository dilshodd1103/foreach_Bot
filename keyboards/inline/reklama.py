from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def reklama_user_keyboard(users, selected_users):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for user in users:
        user_id = user['telegram_id']
        username = user['username']
        if isinstance(selected_users, int):
            selected_users = [selected_users]
        if user_id in selected_users:
            button_text = f"✅ {username}"
        else:
            button_text = username
        keyboard.insert(InlineKeyboardButton(text=button_text, callback_data=f"user_{user_id}"))
    keyboard.row(
        InlineKeyboardButton(text="✅ Yuborish", callback_data="send"),
        InlineKeyboardButton(text="◀️ Ortga", callback_data="cancel")
    )
    return keyboard
