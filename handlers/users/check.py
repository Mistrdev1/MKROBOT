from aiogram import types
from loader import dp, db, bot
from keyboards.default.buttons import *
from datetime import date, timedelta, datetime
from utils.texts import ESLATMA_MATNI


@dp.callback_query_handler(text_contains="checked:")
async def checkadminhandler(call: types.CallbackQuery):
    datas = call.data.rsplit(":")[1]
    try:
        now = datetime.now()
        date = now.date()
        db.update_user_subs(
            subscription="True",
            user_id=datas
        )
        db.update_user_subs_date(
            subscription_on=date,
            user_id=datas
        )
    except Exception as err:
        await bot.send_message(
            chat_id=1849953640,
            text=f"ADMIN CHECK ERROR1: {err}"
        )
    try:
        subs_month = int(db.get_subs_month(
            user_id=datas
        )[0])
        month_datas = db.get_month(
            id=subs_month
        )
        if month_datas[1] == "Bir oy":
            kunlar = 1
        if month_datas[1] == "Ikki oy":
            kunlar = 2
        if month_datas[1] == "Doimiy":
            kunlar = 12
        today = date.today()
        six_months = timedelta(days=30*kunlar)
        future_date = today + six_months
        future_date_formatted = future_date.strftime("%Y-%m-%d %H:%M:%S")
        db.update_subscription_off(
            subscription_off=future_date_formatted,
            user_id=datas
        )
        try:
            await bot.send_message(
                chat_id=datas,
                text=f"<i><b>🎉 Sizning {month_datas[1]} obunangiz muvaffaqiyatli tasdiqlandi,\nEndi botdan to'laqonli foydalanishingiz mumkin.😊 ✅</b></i>",
                reply_markup=second_menu
            )
            await bot.send_message(
                chat_id=datas,
                text=ESLATMA_MATNI,
                reply_markup=second_menu
            )
        except Exception as err:
            await bot.send_message(
                chat_id=1849953640,
                text=f"ADMIN CHECK ERROR2: {err}"
            )
            await call.message.asnwer("Xatolik ketdi, dasturchi bilan bog'laning.")
    except Exception as err:
        await bot.send_message(
            chat_id=1849953640,
            text=f"ADMIN CHECK ERROR2: {err}"
        )
        await call.message.asnwer("Xatolik ketdi, dasturchi bilan bog'laning.")

    # await call.message.edit_text(text="\n\nTasdiqlangan ✅")
    await call.message.delete_reply_markup()
    await call.answer("Tasdiqlandi ✅", show_alert=True)


@dp.callback_query_handler(text_contains="rejected:")
async def rejected_handler(call: types.CallbackQuery):
    datas = call.data.rsplit(":")[1]
    try:
        db.update_user_subs(
            subscription="False",
            user_id=datas
        )
        await bot.send_message(
            chat_id=datas,
            text="<b>Sizning obunangiz tasdiqlanmadi ❌,\niltimos qaytadan urinib ko'ring.🔄</b>",
            reply_markup=main_menu
        )
        await call.message.delete_reply_markup()
        await call.answer("Rad etildi ❌", show_alert=True)
    except Exception as err:
        await bot.send_message(
            chat_id=1849953640,
            text=f"ADMIN CHECK ERROR1: {err}"
        )
