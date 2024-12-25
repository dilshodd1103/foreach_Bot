import datetime
import pytz

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.admin_menu import admin
from keyboards.default.all_user import all_user
from data.config import ADMINS
from keyboards.default.menu import menu
from keyboards.inline.kurslar import kurslar
from loader import dp, db, bot


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Menu")
async def menu1(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b>Foydalanuvchilar menusi : </b>", reply_markup=menu)


@dp.message_handler(text='Foydalanuvchilar soni')
async def all_users(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        data = await db.count_users()
        await msg.answer(f"<b>Foydalanuvchilar soni: </b>{data}", reply_markup=all_user)
        await state.set_state('users_get')

@dp.message_handler(state='users_get', text='◀️Ortga')
async def user_back(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("Admin menu", reply_markup=admin)
        try:
            await state.finish()
        except:
            pass

@dp.message_handler(state='users_get', text="Foydalanuvchilarni ko'rish")
async def all_user_id(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        data = await db.select_all_users()
        await msg.answer("<b>Barcha foydalanuvchilar</b>", reply_markup=kurslar(data))
        await msg.answer(f"<b>Qaytish uchun <i>Ortga</i> tugmasini bosing : </b>", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state('seen_user')

@dp.callback_query_handler(text='back', state='seen_user')
async def back_to_back(call: types.CallbackQuery, state: FSMContext):
    if await is_user_admin(call.from_user.id):
        await call.message.answer('Ortga', reply_markup=all_user)
        await state.set_state('users_get')

@dp.callback_query_handler(regexp="wrong_number+")
async def xato_raqam(call: types.CallbackQuery):
    id = call.data.split(':')[1]
    answer = f"<b>Botga kiritgan raqamingiz orqali sizga bog'lana olmadik\n\nIltimos, sizga bog'lana olishimiz mumkin bo'lgan raqamingizni botga kiriting❗️</b>"
    await bot.send_message(id, answer)
    message = call.message.html_text
    t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    time = t.strftime("%H:%M %d.%m.%Y")
    answer = f"{message}\n\n<b>Ko'rib chiqildi : </b>\n<i>Noto'g'ri raqam ❌\n\n{time}</i>"
    admins = await db.get_admin()
    if admins:
        for admin in admins:
            admin_id = admin['telegram_id']
            await bot.send_message(admin_id, answer)

@dp.callback_query_handler(text="ok")
async def ok(call: types.CallbackQuery):
    message = call.message.html_text
    t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    time = t.strftime("%H:%M %d.%m.%Y")
    answer = f"{message}\n\n<b>Ko'rib chiqildi </b>✅\n\n<i>{time}</i>"
    admins = await db.get_admin()
    if admins:
        for admin in admins:
            admin_id = admin['telegram_id']
            await bot.send_message(admin_id, answer)