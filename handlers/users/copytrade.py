from aiogram import types
from data.config import DEVELOPER
from loader import dp, bot, db
from keyboards.default.buttons import copy_trade_buttons
from keyboards.inline.copy_trade import notification_config_buttons, channels_copy_trade
from utils.texts import COPY_TRADE_INFO


@dp.message_handler(text="💎 Copy Trade")
async def copy_trade_main_handler(message: types.Message):
    await message.answer("<i>Marhamat kerakli tugmani bosing 👇</i>", reply_markup=copy_trade_buttons)


@dp.message_handler(text="📊 Long/Short")
async def copy_trade_notifications(message: types.Message):
    await message.answer("<b>⚙️ Bildirishnomalarni sozlash.</b>", reply_markup=notification_config_buttons(user_id=message.from_user.id))


@dp.callback_query_handler(text_contains="notification_")
async def callback_trade(call: types.CallbackQuery):
    datas = call.data.split("_")
    if datas[1] == "on":
        try:
            db.update_notification_status(
                trade_notification="True",
                user_id=call.from_user.id,
            )
            await call.message.edit_reply_markup(
                reply_markup=notification_config_buttons(
                    user_id=call.from_user.id
                )
            )
            await call.answer("✅ Long/Short uchun bildirishnomalar yoqildi.", show_alert=True)
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti.", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"Long/Short bildirishnomalarini yoqishda xatolik ketdi: {err}"
            )
    if datas[1] == "off":
        try:
            db.update_notification_status(
                trade_notification="False",
                user_id=call.from_user.id,
            )
            await call.message.edit_reply_markup(
                reply_markup=notification_config_buttons(
                    user_id=call.from_user.id
                )
            )
            await call.answer("❌ Long/Short uchun bildirishnomalar o'chirildi.", show_alert=True)
        except Exception as err:
            await call.answer("⚙️ Botda texnik ishlar olib borilayapti. Iltimos biroz vaqtdan keyin urinib koring.", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"Long/Short bildirishnomalarini o'chirishda xatolik ketdi: {err}"
            )



@dp.message_handler(text="💎 Copy Trade kanallar")
async def copy_trade_notifications(message: types.Message):
    await message.answer("<b>📊 Kanalni tanlang: </b>", reply_markup=channels_copy_trade)



@dp.message_handler(text="ℹ️ Copy Trade haqida")
async def infotrade(message: types.Message):
    await message.answer(text=COPY_TRADE_INFO)




@dp.callback_query_handler(text = "choose_trader")
async def copy_trade_trader(call: types.CallbackQuery):
    text = (call.message.text).split(" ")
    try: 
        if db.check_trader(user_id=call.from_user.id, name=text[0]):
            try:
                db.delete_trader(
                    user_id=call.from_user.id, 
                    name=text[0]
                )
            except Exception as err: print(err)
            await call.answer("Tanlov olib tashlandi ✅", show_alert=True)
        else:
            db.add_trader(
                user_id=call.from_user.id,
                name=text[0]
            )
            await call.answer("Tanlandi ✅", show_alert=True)
    except Exception as err: print(err)
    print(text[0])
