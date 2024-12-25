from aiogram import types

from data.config import ADMINS
from keyboards.default.admin_menu import admin
from loader import dp, db


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Admin")
async def admin_func(msg: types.Message):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("Admin panel", reply_markup=admin)
