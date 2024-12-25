import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu
from keyboards.inline.aloqa import aloqa
from keyboards.inline.aloqaga_chiq import aloqa_keyboard
from keyboards.inline.kurslar import kurslar
from loader import dp, db, bot


@dp.message_handler(text="📚Bizning kurslarimiz")
async def kurss(msg: types.Message, state: FSMContext):
    data = await db.select_all_kurs()
    if data:
        await msg.answer(f"<b>📚Kurslarimiz soni : </b><i>{len(data)} ta</i>", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("<b>📚Bizning kurslarimiz : </b>", reply_markup=kurslar(data))
        await state.set_state('kurslar')
    else:
        await msg.answer("<b>Kurslar mavjud emas</b>")


@dp.callback_query_handler(text="back", state='kurslar')
async def menuu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<i>Menu : </i>", reply_markup=menu)
    user_id = call.from_user.id
    await db.save_user_action(user_id)
    try:
        await state.finish()
    except KeyError:
        pass


@dp.message_handler(state="kurslar")
async def messagee(msg: types.Message):
    await msg.delete()
    await msg.answer("<b>Bosh menuga qaytish uchun 🔙Ortga tugmasini bosing.</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, (msg.message_id + 1))


@dp.callback_query_handler(state='kurslar')
async def tarif(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = int(call.data)
    kurs = await db.select_kurs(data)
    user = await db.select_user(call.from_user.id)

    # Rasmni olish
    kurs_nomi, tarif, rasm = kurs[1], kurs[2], kurs[4]

    # Rasm bor yoki yo'qligini tekshirish
    if rasm:
        # Kurs nomi, rasm va tarifni yuborish
        await bot.send_photo(call.from_user.id, rasm, caption=f"<b>📕Kurs nomi: {kurs_nomi}</b>\n\n{tarif}")
    else:
        # Faqat kurs nomi va tarifni yuborish
        await call.message.answer(f"<b>📕Kurs nomi: {kurs_nomi}</b>\n\n{tarif}")

    # Aloqa tugmasini yuborish
    answer = (
        f"<i>📕Kurs haqida qo'shimcha ma'lumot olishni istasangiz, operatorimiz siz bilan bog'lanishi mumkin.\n"
        f"Buning uchun quyidagi tugmani bosing :\n\n"
        f"*Sizning raqamingiz : <u>{user[3]}</u>, boshqa raqamga qo'ng'iroq qilishimizni xohlasangiz "
        f"🛠Sozlamalar bo'limidan raqamingizni o'zgartiring.</i>"
    )
    await call.message.answer(answer, reply_markup=aloqa(f"aloqa:{kurs_nomi}"), disable_web_page_preview=True)
    await call.message.answer("<i>Menu : </i>", reply_markup=menu)
    user_id = call.from_user.id
    await db.save_user_action(user_id)
    try:
        await state.finish()
    except KeyError:
        pass


@dp.callback_query_handler(regexp="aloqa:+")
async def aloqa1(call: types.CallbackQuery):
    kurs = call.data.split(":")[1]
    user = await db.select_user(call.from_user.id)
    username = call.from_user.username
    if not username:
        username = "Username mavjud emas"
    else:
        username = f"@{username}"
    answer = (
        f"<b>Foydalanuvchi <u>{user[1]}</u>  <u>{kurs}</u> kursi uchun aloqaga chiqishni so'radi\n\n"
        f"Telefon raqam : <i>{user[3]}</i>\nUsername : <i>{username}</i></b>"
    )
    await call.message.answer(
        f"<b>{kurs} kursi bo'yicha so'rovingiz yuborildi✅\n\n"
        f"<i>Operatorlarimiz tez orada <u>{user[3]}</u> raqamingizga aloqaga chiqishadi.</i></b>"
    )
    await call.message.delete()
    admins = await db.get_admin()
    if admins:
        for admin in admins:
            admin_id = admin['telegram_id']
            await bot.send_message(admin_id, answer, reply_markup=aloqa_keyboard(call.from_user.id))
