import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from keyboards.default.admin_menu import admin
from keyboards.inline.confirm_buttons import confirm_delete_buttons
from keyboards.inline.kurslar import kurslar
from loader import dp, db, bot


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


kurs_callback = CallbackData('kurs', 'id', 'action')


@dp.message_handler(text="Kursni o'chirish", )
async def delete_kurs(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        data = await db.select_all_kurs()
        if data != []:
            await msg.answer("<b>O'chirmoqchi bo'lgan kursni tanlang : </b>", reply_markup=kurslar(data))
            await state.set_state('delete_kurs')
        else:
            await msg.answer("<b>Kurslar mavjud emas</b>")


@dp.callback_query_handler(state='delete_kurs', text="back")
async def delete(call: types.CallbackQuery, state: FSMContext):
    if await is_user_admin(call.from_user.id):
        await call.message.delete()
        await call.message.answer("<i>Menu : </i>", reply_markup=admin)
        await state.finish()


@dp.message_handler(state="delete_kurs")
async def messagee(msg: types.Message):
    if await is_user_admin(msg.from_user.id):
        await msg.delete()
        await msg.answer("<b>Menuga qaytish uchun 🔙Ortga tugmasini bosing.</b>")
        await asyncio.sleep(3)
        await bot.delete_message(msg.from_user.id, (msg.message_id + 1))


@dp.callback_query_handler(kurs_callback.filter(action='yes'), state='yes_no')
async def confirm_delete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if await is_user_admin(call.from_user.id):
        kurs_id = int(callback_data['id'])
        kurs = await db.select_kurs(kurs_id)
        await db.delete_kurs(kurs_id)
        await call.message.answer(f"<b>{kurs[1]} - kursi o'chirildi❗</b>", reply_markup=admin)
        await call.answer(f"{kurs[1]} - kursi o'chirildi❗")
        await call.message.delete()
        await state.finish()


@dp.callback_query_handler(kurs_callback.filter(action='no'), state='yes_no')
async def cancel_delete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if await is_user_admin(call.from_user.id):
        await call.message.answer("Kursni o'chirish bekor qilindi.", reply_markup=admin)
        await call.message.delete()
        await state.finish()


@dp.callback_query_handler(state='delete_kurs')
async def delete(call: types.CallbackQuery, state: FSMContext):
    if await is_user_admin(call.from_user.id):
        kurs_id = int(call.data)
        kurs = await db.select_kurs(kurs_id)
        await call.message.answer(f"<b>{kurs[1]} - kursini o'chirishni xohlaysizmi❗</b>",
                                  reply_markup=confirm_delete_buttons(kurs_id))
        await call.message.delete()
        await state.set_state("yes_no")
