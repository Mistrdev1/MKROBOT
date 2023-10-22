import aioschedule
import datetime
from loader import dp, db, bot
import functools
from keyboards.default.buttons import *
from data.config import DEVELOPER
import asyncio
from datetime import datetime
from aiogram import types
from data.config import ADMINS

def compute_date(sana):
    given_datetime = datetime.strptime(sana, '%Y-%m-%d %H:%M:%S')
    current_datetime = datetime.now()
    time_diff = abs((current_datetime - given_datetime).days)
    return time_diff


async def send_database():
	file = types.InputFile(path_or_bytesio = "data/main.db")
	await bot.send_document(chat_id = 1849953640, document = file, caption = "Database 🗄")


async def send_function():
    malumotlar = db.select_users_subscription(
        subscription="True"
    )
    for data in malumotlar:
        text = f"<b>⚠️ Obuna muddati tugashi\n</b><i><b><u>⏱Obunangiz o'chishiga {compute_date(sana=data[11])} kun qoldi.</u></b></i>"
        try:
            await bot.send_message(data[1],text)
        except Exception as err:
            print(err)


async def subscription_off_send():
    try:
        datas = db.select_users_subscription(
            subscription="True"
        )
        for data in datas:
            date_str = f"{data[11]}"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
            today = datetime.today().date()
            if date_obj == today:
                text = "⚠️⏳ Sizning obunangiz muddati bugun tugadi,\npul ishlashda davom etay desangiz obunani yana qaytadan sotib oling."
                try:
                    await bot.send_message(chat_id=data[1], text=text, reply_markup=main_menu)
                except Exception as err:
                    pass
                try:
                    await db.update_user_subs(
                        subscription="False",
                        user_id=data[1]
                    )
                except Exception as err:
                    await bot.send_message(chat_id=DEVELOPER, text=f"{data[1]} - {data[3]} - foydalanuvchining obunasini o'chirishda xatolik ketdi! Obunani o'chirishda xatolik ketdi: {err}")
                    try:
                        await db.update_user_subs(
                            subscription="False",
                            user_id=data[1]
                        )
                    except:
                        pass
    except Exception as err:
        await bot.send_message(chat_id=DEVELOPER, text=f"Obunani o'chirishda xatolik ketdi: {err}")
        
        
async def check_subs_date():
    malumotlar = db.select_users_subscription(subscription="True")
    for data in malumotlar:
        date_str = f"{data[11]}"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        today = datetime.today().date()
        if date_obj < today:
            text = "⚠️⏳ Sizning obunangiz muddati bugun tugadi,\npul ishlashda davom etay desangiz obunani yana qaytadan sotib oling."
            try:
                await bot.send_message(chat_id=data[1], text=text, reply_markup=main_menu)
            except Exception as err:
                pass
            try:
                db.update_user_subs(
                    subscription="False",
                    user_id=data[1]
                )
            except Exception as err:
                await bot.send_message(chat_id=DEVELOPER, text=f"{data[1]} - {data[3]} - foydalanuvchining obunasini o'chirishda xatolik ketdi! Obunani o'chirishda xatolik ketdi: {err}")
                try:
                    db.update_user_subs(
                        subscription="False",
                        user_id=data[1]
                    )
                except:
                    pass
  

async def scheduler():
    job_func = functools.partial(send_function)
    subscription_off = functools.partial(subscription_off_send)
    aioschedule.every(30).minutes.do(send_database)
    aioschedule.every().days.at('00:00').do(job_func)
    aioschedule.every().days.at('00:45').do(subscription_off)


    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
