from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin_menu import admin
from keyboards.default.get_admin import get_admin
from keyboards.inline.admin import adminlar
from keyboards.inline.getAdmin import admin_list_keyboard
from loader import db
from loader import dp


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Adminlar")
async def admins(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        try:
            await msg.answer("<b>Adminlar bilan ishlash:</b>", reply_markup=get_admin)
            await state.set_state("admin0")
        except NotImplementedError as e:
            await msg.answer("Sizda buning uchun ruxsat yo'q")


@dp.message_handler(text="Ortga", state="admin0")
async def back_admin(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b>Admin menu:</b>", reply_markup=admin)
        try:
            await state.finish()
        except KeyError:
            pass


@dp.message_handler(text="Admin tayinlash", state="admin0", chat_id=ADMINS)
async def get_user(msg: types.Message, state: FSMContext):
    data = await db.select_all_users()
    if data:
        await msg.answer(f"<b>Obunachilar soni:</b> <i>{len(data)} ta</i>", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("<b>Admin tayinlang :</b>", reply_markup=adminlar(data))
        await state.set_state('admin1')
    else:
        await msg.answer("<b>Obunachilar mavjud emas</b>")


@dp.callback_query_handler(text="back1", state='admin1', chat_id=ADMINS)
async def menuu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<i>Adminlar bilan ishlash:</i>", reply_markup=get_admin)
    await state.set_state('admin0')


@dp.callback_query_handler(lambda c: c.data.startswith('page_'), state='admin1', chat_id=ADMINS)
async def handle_page(call: types.CallbackQuery):
    page = int(call.data.split('_')[1])
    listt = await db.get_all_users()
    kurs = adminlar(listt, page)
    await call.message.edit_text("🔑 Foydalanuvchilar ro'yxati:", reply_markup=kurs)
    await call.answer()


@dp.callback_query_handler(state='admin1', chat_id=ADMINS)
async def tarif(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    selected_data = int(call.data)
    is_admin = await db.check_admin(selected_data)

    if is_admin:
        await call.message.answer(f"<b>⚠️ Foydalanuvchi allaqachon admin!</b>", reply_markup=admin)
    else:
        await db.set_admin(selected_data)
        await call.message.answer(f"<b>✅ Foydalanuvchi admin sifatida belgilandi.</b>", reply_markup=admin)
    try:
        await state.finish()
    except KeyError:
        pass


@dp.message_handler(text="Adminlarni ko'rish", state="admin0", chat_id=ADMINS)
async def remove(msg: types.Message, state: FSMContext):
    data = await db.get_admin()
    admins = [user for user in data if user['admin']]

    if not admins:
        await msg.answer("Hozirda hech qanday admin topilmadi.")
        return
    keyboard = admin_list_keyboard(admins)
    await msg.answer(f"<b>Adminlarimiz soni : </b><i>{len(data)} ta</i>", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(f"<b>Adminlikdan olib tashlash uchun ustiga bosing: </b>", reply_markup=keyboard)
    try:
        await state.finish()
    except KeyError:
        pass


@dp.callback_query_handler(text="qaytish")
async def qaytish(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("<b>Adminlar bilan ishlash:</b>", reply_markup=get_admin)
    await state.set_state('admin0')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("remove_admin_"), chat_id=ADMINS)
async def remove_admin_handler(call: types.CallbackQuery, state: FSMContext):
    admin_id = int(call.data.split("_")[-1])
    success = await db.remove_admin(admin_id)

    if success:
        await call.message.answer(
            f"<b>Admin <i>{call.from_user.full_name}</i> adminlikdan olib tashlandi.</b>", reply_markup=admin)
    else:
        await call.message.answer(
            "Xatolik yuz berdi, iltimos keyinroq urinib ko'ring.", reply_markup=admin)
    await call.answer()
    try:
        await state.finish()
    except:
        pass
