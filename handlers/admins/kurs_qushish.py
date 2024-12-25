from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from loader import dp, db, temp


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


# O‘tkazib yuborish va ortga tugmalarini yaratish
optional_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
optional_buttons.add(KeyboardButton("⬇️O‘tkazib yuborish"), KeyboardButton("◀️Ortga"))


@dp.message_handler(Text(equals="Kurs qo'shish"))
async def add_kurs(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b>Kurs nomini yuboring : </b>", reply_markup=bekor)
        await state.set_state("kurs_nomi")


@dp.message_handler(Text(equals="◀️Ortga"), state="kurs_nomi")
async def back_to_menu(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b><i>Menu : </i></b>", reply_markup=admin)
        try:
            await state.finish()
        except KeyError:
            pass

@dp.message_handler(Text(equals="◀️Ortga"), state= "kurs_tarif")
async def back_to_menu(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b><i>Kurs uchun rasm yuboring : </i></b>", reply_markup=optional_buttons)
        await state.set_state('kurs_rasm')

@dp.message_handler(Text(equals="◀️Ortga"), state= "kurs_rasm")
async def back_to_menu(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b><i>Kursga nomini kiriting : </i></b>", reply_markup=bekor)
        await state.set_state('kurs_nomi')

@dp.message_handler(state="kurs_nomi")
async def add_nom(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        if len(msg.text) < 255:
            temp[msg.from_user.id] = {"kurs_nomi": msg.text}
            await msg.answer("<b>Kurs uchun rasmni yuboring yoki “⬇️O‘tkazib yuborish” tugmasini bosing:</b>",
                             reply_markup=optional_buttons)
            await state.set_state("kurs_rasm")
        else:
            await msg.answer("<b>Juda uzun, qayta kiriting : (255 ta belgi)</b>", reply_markup=bekor)


@dp.message_handler(Text(equals="⬇️O‘tkazib yuborish"), state="kurs_rasm")
async def skip_kurs_rasm(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b>Kurs ta'rifini yuboring :</b>", reply_markup=bekor)
        await state.set_state("kurs_tarif")


@dp.message_handler(content_types=types.ContentType.PHOTO, state="kurs_rasm")
async def add_kurs_rasm(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        kurs_data = temp.get(msg.from_user.id, {})
        if kurs_data.get("kurs_nomi"):
            file_id = msg.photo[-1].file_id  # Eng yuqori sifatli rasmni olish
            kurs_data["kurs_rasm"] = file_id
            temp[msg.from_user.id] = kurs_data
            await msg.answer("<b>Kurs ta'rifini yuboring :</b>", reply_markup=bekor)
            await state.set_state("kurs_tarif")
        else:
            await msg.answer("<b>Xatolik: Kurs nomini kiritmagan bo'lishingiz mumkin.</b>", reply_markup=admin)
            try:
                await state.finish()
            except KeyError:
                pass


@dp.message_handler(state="kurs_tarif")
async def add_kurs_tarif(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        try:
            kurs_data = temp.get(msg.from_user.id, {})
            kurs_nomi = kurs_data.get("kurs_nomi")
            kurs_rasm = kurs_data.get("kurs_rasm", None)  # Rasm bo'lmasa `None` qaytaradi
            if kurs_nomi:
                await db.add_kurs(kurs_nomi, msg.html_text, kurs_rasm)
                await msg.answer("<b>Kurs muvaffaqiyatli qo'shildi ✅</b>", reply_markup=admin)
                temp.pop(msg.from_user.id, None)  # Tempdan foydalanuvchi ma'lumotlarini olib tashlash
            else:
                await msg.answer("<b>Xatolik: Ma'lumotlar to'liq emas.</b>", reply_markup=admin)
            try:
                await state.finish()
            except KeyError:
                pass
        except Exception as e:
            await msg.answer("<b>Xatolik ❗️\n\n<i>Bunday nomdagi kurs bo'lishi mumkin, tekshirib ko'ring</i></b>",
                             reply_markup=admin)
            try:
                await state.finish()
            except KeyError:
                pass
