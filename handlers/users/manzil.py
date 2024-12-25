from aiogram import types

from loader import dp, db


@dp.message_handler(text="📍Manzilimiz")
async def manzil(msg: types.Message):
    await msg.answer("<b>🏢 Qarshi shahar, </b>")
    user_id = msg.from_user.id
    await db.save_user_action(user_id)


@dp.message_handler(text="🔗Biz bilan bog'lanish")
async def boglan(msg: types.Message):
    await msg.answer("<b>Murojaat uchun telefon raqamlari :\n\n☎️+998940500093\n☎️+998946389778</b>")
    user_id = msg.from_user.id
    await db.save_user_action(user_id)