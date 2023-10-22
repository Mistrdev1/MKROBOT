from aiogram.types import CallbackQuery
from data.config import ADMINS
from loader import dp, db
from utils.db_api.dbxl import check_trans


@dp.callback_query_handler(text_contains="trans_success:", state="*")
async def status1(call: CallbackQuery):
    if call.from_user.id == ADMINS[0]:
        user_tgid = call.data.replace("trans_success:", "")
        try:
            datas = db.get_transfer_data(
                user_id=user_tgid
            )
            infos = db.select_user_info(
                user_id=user_tgid
            )
            MATN = f"🤖: @MKSIGNAL_RoBot\n"
            MATN += f"🆔: {datas[0]}\n"
            MATN += f"👤: {infos[3]}\n"
            MATN += f"🔀: {datas[2]}\n"
            MATN += f"📥: {datas[3]}\n"
            MATN += f"🔎 Status: ✅\n"
            MATN += f"💰: {datas[6]}"
            TEXT = f"ID: {datas[0]}\n✅Sizning almashuvingiz <b>Muvaffaqiyatli</b> yakunlandi\n"
            await dp.bot.send_message(
                chat_id=user_tgid,
                text=TEXT
            )
            await dp.bot.send_message(
                chat_id=-1001667916888,
                text=MATN
            )
        except:
            pass
        await call.message.delete()
    else:
        await call.answer("Siz admin emassiz!", show_alert=True)


@dp.callback_query_handler(text_contains="trans_fail:", state="*")
async def status2(call: CallbackQuery):
    if call.from_user.id == ADMINS[0]:
        user_tgid = call.data.replace("trans_fail:", "")
        trans_id = call.message.text[13:16]
        TEXT = f"❌Sizning so'rovingiz <b>Rad etildi!</b>\nSiz berilgan raqamga to'lov qilmagansiz"

        try:
            await dp.bot.send_message(chat_id=user_tgid, text=TEXT)
        except:
            pass
        await call.message.delete()
    else:
        await call.answer("Siz admin emassiz!", show_alert=True)
