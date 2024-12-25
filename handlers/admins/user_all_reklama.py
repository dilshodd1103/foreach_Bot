import asyncio
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter

from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from loader import dp, db, bot


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Reklama")
async def reklama(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer(
            "<b>Yaxshi, reklama postini yuboring : </b>\n<i>(Text, Rasm, Video, Dokument)</i>\n<i>❗️Yuborgan postingiz shu holicha barcha foydalanuvchilarga yuboriladi\nOrtga qaytishingiz ham mumkin</i>",
            reply_markup=bekor)
        await state.set_state("r")


@dp.message_handler(text="◀️Ortga", state="r")
async def ortga(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        await msg.answer("<b><i>Menu : </i></b>", reply_markup=admin)
        try:
            await state.finish()
        except:
            pass


@dp.message_handler(state="r", content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT,
                                              types.ContentType.DOCUMENT])
async def reklama2(msg: types.Message, state: FSMContext):
    if await is_user_admin(msg.from_user.id):
        content_type = msg.content_type
        content = ""
        if content_type == types.ContentType.TEXT:
            content = msg.text
        elif content_type == types.ContentType.PHOTO:
            content = msg.photo[-1].file_id
        elif content_type == types.ContentType.VIDEO:
            content = msg.video.file_id
        elif content_type == types.ContentType.DOCUMENT:
            content = msg.document.file_id

        data_users = await db.select_all_users()
        n = 0
        successful = 0

        for user in data_users:
            try:
                user_id = user[6]
                await bot.copy_message(chat_id=user_id, from_chat_id=msg.from_user.id, message_id=msg.message_id)
                successful += 1
            except BotBlocked:
                n += 1
            except ChatNotFound:
                n += 1
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
            except Exception as e:
                n += 1
            finally:
                await asyncio.sleep(0.1)
        await msg.answer(f"<b>✅Yuborildi : <i>{successful}</i>\n❌Yuborilmadi : <i>{n}</i></b>", reply_markup=admin)
        await db.add_admin_reklama(content_type=content_type, content=content, sent_date=datetime.now(),
                                   send_to_all=successful)
        try:
            await state.finish()
        except:
            pass
