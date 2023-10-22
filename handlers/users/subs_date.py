from aiogram import types
from loader import db, dp, bot
import datetime


def compute_date(sana):
    given_datetime = datetime.datetime.strptime(sana, '%Y-%m-%d %H:%M:%S')
    current_datetime = datetime.datetime.now()
    time_diff = abs((current_datetime - given_datetime).days)
    return time_diff


@dp.message_handler(text="⏰ Obuna muddati")
async def date_offhandler(message: types.Message):
    if db.get_user_subs(user_id=message.from_user.id)[0] == "True":
        malumotlar = db.select_user_datas(user_id=message.from_user.id)
        text = "<b>⚙️Obunangiz haqida malumotlar 👇</b>\n\n"
        datas = db.get_month(id=malumotlar[9])
        text += f"<i>📆Obunangiz muddati:</i> <b>{datas[1]}</b>\n"
        text += f"<i>💵Obunangiz narxi:</i> <b>{datas[2]}\n</b>"
        text += f"<i>⏰Siz obunani sotib olgan sana:</i> <b>{malumotlar[10]}</b>\n"
        text += f"<i>⌛️Obuna o'chadigan sana:</i> <b>{malumotlar[11]}</b>\n\n"
        text += f"<i><b><u>⏱Obuna o'chishiga {compute_date(sana=malumotlar[11])} kun qoldi.</u></b></i>"
        rasm = types.InputFile(path_or_bytesio="photos/image.jpg")
        await message.answer_photo(photo=rasm, caption=text)
        print(malumotlar[10], malumotlar[11])
