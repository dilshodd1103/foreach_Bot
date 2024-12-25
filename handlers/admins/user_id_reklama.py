import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter

from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from keyboards.inline.reklama import reklama_user_keyboard
from loader import dp, db, bot


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Alohida xabar")
async def start_reklama(msg: types.Message, state: FSMContext):
    """Reklama xabarini boshlash"""
    if await is_user_admin(msg.from_user.id):
        await msg.answer(
            "<b>Yaxshi, reklama postini yuboring : </b>\n<i>(Text, Rasm, Video, Dokument)</i>\n"
            "❗️<i>Tanlangan foydalanuvchilarga yuboriladi</i>",
            reply_markup=bekor)
        await state.set_state("waiting_for_reklama")


@dp.message_handler(state="waiting_for_reklama", text="◀️Ortga")
async def back_reklama(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Admin menu</b>", reply_markup=admin)
    try:
        await state.finish()
    except:
        pass


@dp.message_handler(state="waiting_for_reklama", content_types=[
    types.ContentType.TEXT,
    types.ContentType.PHOTO,
    types.ContentType.VIDEO,
    types.ContentType.DOCUMENT
])
async def save_reklama(msg: types.Message, state: FSMContext):
    """Reklama xabarini saqlash va foydalanuvchilarni tanlash"""
    if await is_user_admin(msg.from_user.id):
        await state.update_data(
            content_type=msg.content_type,
            message_id=msg.message_id,
            chat_id=msg.from_user.id,
            selected_users=[]
        )
        users = await db.select_all_users()
        data = msg.from_user.id
        keyboard = reklama_user_keyboard(users, data)
        await msg.answer(
            "<b>Foydalanuvchilarni tanlang yoki <i>◀️ Ortga</i> tugmasini bosing:</b>",
            reply_markup=keyboard
        )
        await state.set_state("waiting_for_user_selection")


@dp.callback_query_handler(state="waiting_for_user_selection")
async def handle_user_selection(call: types.CallbackQuery, state: FSMContext):
    """Foydalanuvchini tanlash yoki jarayonni bekor qilish"""
    if await is_user_admin(call.from_user.id):
        data = await state.get_data()
        selected_users = data.get("selected_users", [])

        if call.data == "cancel":
            await call.message.answer("<b>Xabarni qayta yuboring\n Yoki <i>ortga</i> qayting.</b>", reply_markup=bekor)
            await state.set_state('waiting_for_reklama')

        elif call.data == "send":
            if not selected_users:
                await call.message.answer("<b>Hech qanday foydalanuvchi tanlanmagan!</b>")
                return

            content_type = data.get("content_type")
            message_id = data.get("message_id")
            from_chat_id = data.get("chat_id")

            successful = 0
            failed = 0
            for user_id in selected_users:
                try:
                    await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id)
                    successful += 1
                except (BotBlocked, ChatNotFound):
                    failed += 1
                except RetryAfter as e:
                    await asyncio.sleep(e.timeout)
                except Exception as e:
                    failed += 1
                finally:
                    await asyncio.sleep(0.1)

            await call.message.answer(
                f"<b>✅ Yuborildi: {successful}\n❌ Yuborilmadi: {failed}</b>",
                reply_markup=admin
            )
            try:
                await state.finish()
            except:
                pass

        elif call.data.startswith("user_"):
            user_id = int(call.data.split("_")[1])

            if user_id not in selected_users:
                selected_users.append(user_id)
                await state.update_data(selected_users=selected_users)
                await call.answer("Foydalanuvchi tanlandi ✅")
            else:
                selected_users.remove(user_id)
                await state.update_data(selected_users=selected_users)
                await call.answer("Foydalanuvchi olib tashlandi ❌")

            users = await db.select_all_users()
            keyboard = reklama_user_keyboard(users, selected_users)
            await call.message.edit_reply_markup(reply_markup=keyboard)
