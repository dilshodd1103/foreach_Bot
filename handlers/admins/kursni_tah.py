from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from keyboards.default.kurs_tahrirlash import kurs_tahriri
from keyboards.inline.kurslar import kurslar
from loader import dp, db, bot


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


# Kursni tahrirlashni boshlash
@dp.message_handler(text="Kursni tahrirlash")
async def edit_course(msg: types.Message, state: FSMContext):
    if not await is_user_admin(msg.from_user.id):
        return await msg.answer("<b>Siz admin emassiz!</b>")

    courses = await db.select_all_kurs()
    if courses:
        await msg.answer('<b>Kursni tahrirlash</b>', reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("<b>Tahrirlamoqchi bo'lgan kursni tanlang:</b>", reply_markup=kurslar(courses))
        await state.set_state('edit_kurs')
    else:
        await msg.answer("<b>Kurslar mavjud emas</b>")


@dp.callback_query_handler(state='edit_kurs')
async def select_course(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back":
        await call.message.answer("Admin menu", reply_markup=admin)
        await state.finish()
    else:
        try:
            course_id = int(call.data)
            kurs = await db.select_kurs(course_id)
            if kurs:
                await state.update_data(course_id=course_id)
                await call.message.answer("<b>Qaysi ma'lumotni tahrirlamoqchisiz?</b>", reply_markup=kurs_tahriri)
                await state.set_state("edit_option")
            else:
                await call.message.answer("<b>Kurs topilmadi!</b>", reply_markup=admin)
                await state.finish()
        except ValueError:
            await call.message.answer("<b>Xato: noto‘g‘ri ma'lumot yuborildi!</b>", reply_markup=admin)
            await state.finish()


@dp.message_handler(state=['edit_name', 'edit_description', 'edit_image'], text="◀️Ortga")
async def ortga_qaytish(msg: types.Message, state: FSMContext):
    await msg.answer("Qaysi ma'lumotni tahrirlamoqchisiz", reply_markup=kurs_tahriri)
    await state.set_state("edit_option")


@dp.message_handler(state=['edit_option'], text="◀️Ortga")
async def back_qaytish(msg: types.Message, state: FSMContext):
    courses = await db.select_all_kurs()
    await msg.answer('<b>Kursni tahrirlash</b>', reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Qaysi kursni tahrirlamoqchisiz", reply_markup=kurslar(courses))
    await state.set_state("edit_kurs")


# Tahrir opsiyasini tanlash
@dp.message_handler(state="edit_option", text=["Kurs nomini", "Kurs tarifini", "Kurs rasmini"])
async def choose_edit_option(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    kurs = await db.select_kurs(data.get("course_id"))

    if msg.text == "Kurs nomini":
        await msg.answer(f"<b>Eski nom:</b> {kurs[1]}\n<b>Yangi nomni yuboring:</b>", reply_markup=bekor)
        await state.set_state("edit_name")
    elif msg.text == "Kurs tarifini":
        await msg.answer(f"<b>Eski tarif:</b> {kurs[2]}\n<b>Yangi tarifni yuboring:</b>", reply_markup=bekor)
        await state.set_state("edit_description")
    elif msg.text == "Kurs rasmini":
        if kurs[4]:
            await bot.send_photo(chat_id=msg.chat.id, photo=kurs[4], caption="<b>Eski rasm:</b>")
            await msg.answer("Kurs uchun yangi rasm yuboring", reply_markup=bekor)
        else:
            await msg.answer("<b>Rasm mavjud emas. Yangi rasmni yuboring:</b>", reply_markup=bekor)
        await state.set_state("edit_image")


# Kurs nomini yangilash
@dp.message_handler(state="edit_name")
async def update_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await db.update_course_name(data.get("course_id"), msg.text)
    await msg.answer("<b>Kurs nomi muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=admin)
    await state.finish()


# Kurs tarifini yangilash
@dp.message_handler(state="edit_description")
async def update_description(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await db.update_tarif(data.get("course_id"), msg.text)
    await msg.answer("<b>Kurs tarifi muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=admin)
    await state.finish()


# Kurs rasmini yangilash
@dp.message_handler(content_types=types.ContentType.PHOTO, state="edit_image")
async def update_image(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_id = msg.photo[-1].file_id
    await db.update_course_image(data.get("course_id"), photo_id)
    await msg.answer("<b>Kurs rasmi muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=admin)
    await state.finish()


# Faqat rasm qabul qilish
@dp.message_handler(state="edit_image")
async def handle_non_photo(msg: types.Message):
    await msg.answer("<b>Iltimos, faqat rasm yuboring.</b>")
