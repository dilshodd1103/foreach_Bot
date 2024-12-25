from aiogram import types

from keyboards.default.menu import menu
from loader import dp, db


@dp.message_handler()
async def asdf(msg: types.Message):
    await msg.answer("<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=menu)
    user_id = msg.from_user.id
    await db.save_user_action(user_id)