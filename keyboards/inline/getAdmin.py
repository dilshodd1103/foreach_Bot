from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def adminlar(users, page=0):
    """Foydalanuvchilarni ro'yxati va sahifalash"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    per_page = 5
    start = page * per_page
    end = start + per_page
    users_on_page = users[start:end]

    for user in users_on_page:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{user['username']} (ID: {user['id']})",
                callback_data=str(user['id'])
            )
        )

    if start > 0:
        keyboard.add(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"page_{page - 1}"))
    if end < len(users):
        keyboard.add(InlineKeyboardButton("Keyingi ➡️", callback_data=f"page_{page + 1}"))

    keyboard.add(InlineKeyboardButton("◀️ Ortga", callback_data="back1"))
    return keyboard

def admin_list_keyboard(admins):
    """Adminlarni ko'rsatish uchun klaviatura"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        keyboard.add(
            InlineKeyboardButton(
                text=f"ID:{admin['id']}   {admin['username']}",
                callback_data=f"remove_admin_{admin['id']}"
            )
        )
    keyboard.add(InlineKeyboardButton("◀️ Ortga", callback_data="qaytish"))
    return keyboard
