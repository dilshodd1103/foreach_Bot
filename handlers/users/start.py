from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg.pgproto.pgproto import timedelta

from data.config import ADMINS
from keyboards.default import menu, contact, til
from loader import dp, db, bot
from utils.misc import belgi


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user = await db.select_user(message.from_user.id)

    if user is None:
        await message.answer(
            "<b><i>Assalomu alaykum! <i>Foreach Education</i> o'quv markazining telegram botiga xush kelibsiz!</i></b>\n"
            "<b>Iltimos, tilni tanlang:</b>",
            reply_markup=til.til
        )
        await state.set_state("til")
    else:
        await message.answer(
            f"<b>Assalomu alaykum <i>{message.from_user.get_mention(message.from_user.full_name)}</i></b>"
        )
        await message.answer("<i>📋Menu : </i>", reply_markup=menu.menu)


@dp.message_handler(state="til")
async def choose_language(msg: types.Message, state: FSMContext):
    language = msg.text.strip().lower()
    if language == "🇺🇿 o'zbekcha" or language == "🇷🇺 русский":
        await state.update_data(language=language)
        await msg.answer("<b>Ism-familiyangizni yuboring : </b>")
        await state.set_state("ism")
    else:
        await msg.answer("<b>Faqat <i>🇺🇿 O'zbekcha</i> yoki <i>🇷🇺 Русский</i> tillarini tanlang!</b>")


@dp.message_handler(state="ism")
async def ismi(msg: types.Message, state: FSMContext):
    if all(x.isalpha() or belgi.belgi(x) for x in msg.text):
        if len(msg.text) < 101 and len(msg.text) > 2:
            await state.update_data(name=msg.text)
            await msg.answer(
                "<b>Raqamingizni yuboring : </b>\n\n❗<b>Siz bilan bog'lana olishimiz uchun, iltimos faol raqamingizni yuboring.</b>\n<i>+998901234567 ko'rinishida yoki shu telegram akkauntingiz raqamidan foydalanayotgan bo'lsangiz </i><u><b>🔢Raqamimni yuborish</b></u><i> tugmasini bosing.</i>",
                reply_markup=contact.contact
            )
            await state.set_state("raqam")
        elif len(msg.text) > 100:
            await msg.answer("<b>Juda uzun, qayta yuboring : </b>")
        else:
            await msg.answer("<b>Juda qisqa qayta yuboring : </b>")
    else:
        await msg.answer(
            "<b>Faqat lotin harflari, bo'sh joy yoki (' `) belgilaridan foydalanishingiz mumkin❗</b>\n\n<i>Qayta kiriting : </i>")


@dp.message_handler(state="raqam")
async def contact_msg(msg: types.Message, state: FSMContext):
    phone_number = msg.text if msg.text.startswith('+998') else None

    if phone_number and len(phone_number) == 13:
        # Raqamni vaqtincha saqlaymiz
        await state.update_data(phone_number=phone_number)
    else:
        await msg.answer("<b>Xato telefon raqami ❗\n\n<i>Iltimos raqamingizni qayta yuboring.</i></b>")
        return  # Telefon raqami noto'g'ri bo'lsa, davom etmaymiz

    user_data = await state.get_data()

    # Foydalanuvchini ma'lumotlar bazasiga qo'shamiz
    await db.add_user(
        telegram_id=msg.from_user.id,
        full_name=user_data['name'],
        username=msg.from_user.username,
        language=user_data['language'],
        phone_num=user_data['phone_number'],
        admin=False,
        joined_at=datetime.now()
    )
    await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>")
    await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
    try:
        await state.finish()
    except:
        pass

    count = await db.count_users()
    data = count if count is not None else 0
    msg = f"{msg.from_user.full_name} bazaga qo'shildi.\nBazada {data} ta foydalanuvchi bor."
    admins = await db.get_admin()
    if admins:
        for admin in admins:
            admin_id = admin['telegram_id']
            await bot.send_message(admin_id, msg)


@dp.message_handler(content_types=types.ContentType.CONTACT, state='raqam')
async def contact_user(msg: types.Message, state: FSMContext):
    raqam = msg.contact.phone_number

    if raqam.startswith("+998"):
        # Raqamni vaqtincha saqlaymiz
        await state.update_data(phone_number=raqam)
    elif raqam.startswith("998"):
        await state.update_data(phone_number=f"+{raqam}")
    else:
        await msg.answer("<b>Xato telefon raqami ❗\n\n<i>Iltimos raqamingizni qayta yuboring.</i></b>")
        return  # Telefon raqami noto'g'ri bo'lsa, davom etmaymiz

    user_data = await state.get_data()

    # Foydalanuvchini ma'lumotlar bazasiga qo'shamiz
    await db.add_user(
        telegram_id=msg.from_user.id,
        full_name=user_data['name'],
        username=msg.from_user.full_name,
        language=user_data['language'],
        phone_num=user_data['phone_number'],
        admin=False,
        joined_at=datetime.now()
    )
    await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>")
    await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
    try:
        await state.finish()
    except:
        pass

    count = await db.count_users()
    data = count if count is not None else 0
    msg = f"{msg.from_user.full_name} bazaga qo'shildi.\nBazada {data} ta foydalanuvchi bor."
    admins = await db.get_admin()
    if admins:
        for admin in admins:
            admin_id = admin['telegram_id']
            await bot.send_message(admin_id, msg)
