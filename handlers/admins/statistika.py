from aiogram import types

from loader import db
from loader import dp
import pytz


async def is_user_admin(user_id: int) -> bool:
    """Adminlikni tekshiruvchi yordamchi funksiya"""
    return await db.check_admin(selected_data=user_id)


@dp.message_handler(text="Statistika")
async def bot_statistic(msg: types.Message):
    if await is_user_admin(msg.from_user.id):
        user = await db.count_users()
        start_user = await db.add_month()
        latest_news_reader = await db.latest_news_reader()
        active_user = await db.get_active_users()
        await db.add_statistic(all_subscribers=user, for_last_month=start_user, latest_news_readers=latest_news_reader)
        result = (f"<b>Obunachilar soni: <i>{user} ta</i>\n\nOxirgi oyda qo'shilganlar: <i>{start_user} ta</i>"
                  f" \n\nOxirgi xabar necha kishiga jo'natilgan: <i>{latest_news_reader} ta</i>\n\n24 soat ichida botdan foydalanganlar: <i>{active_user} ta</i></b>")
        return await msg.answer(result)


@dp.message_handler(text="Ma'lumotlar")
async def is_admin(msg: types.Message):
    if await is_user_admin(msg.from_user.id):
        data = await db.count_admins()
        messege = await db.get_message()
        await db.add_informations(data, messege)
        if messege:
            sent_date = messege
            sent_date = sent_date.astimezone(pytz.timezone('Asia/Tashkent'))
            formatted_date = sent_date.strftime("%d-%m-%Y %H:%M:%S")
            await msg.answer(f"<b>Botdagi Adminlar soni : <i>{data}</i> ta\n\n"
                             f"Eng oxirgi jo'natilgan xabar: {formatted_date}</b>")
