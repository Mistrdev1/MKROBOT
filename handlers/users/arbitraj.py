from data.config import DEVELOPER
from loader import db, dp, bot
from aiogram import types
from keyboards.inline.buttons import *


@dp.message_handler(text="♻️ P2P Arbitraj")
async def psp_handler(message: types.Message):
    await message.answer("Savdo bot menyusi:", reply_markup=p2p_menyu)


@dp.callback_query_handler(text="bekorqilishtugmasiuchun")
async def backtobirjas_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Savdo bot menyusi:",
        reply_markup=p2p_menyu
    )


@dp.callback_query_handler(text="change_spread")
async def change_spred(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Foizni tanglang",
        reply_markup=change_spred_btn(call.from_user.id)
    )


@dp.callback_query_handler(text_contains="change_spred:")
async def change_spred_handler(call: types.CallbackQuery):
    malumotlar = call.data.rsplit(":")
    if malumotlar[1] == "03":
        try:
            db.update_birja(
                birja=0.3,
                user_id=call.from_user.id
            )
            await call.answer(
                text="Spred 0.3 ga muvaffaqiyatli o'zgartirildi ✅ ",
                show_alert=True
            )
            await call.message.answer(
                text="Savdo bot menyusi:",
                reply_markup=p2p_menyu
            )
            await call.message.delete()
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti, iltimos keyinroq urinib ko'ring!", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"✅✅✅✅✅✅✅\n\nBotda birjani UPDATE qilishda xatolik ketdi: {err}\n\n✅✅✅✅✅✅✅"
            )
    if malumotlar[1] == "05":
        try:
            db.update_birja(
                birja=0.5,
                user_id=call.from_user.id
            )

            await call.answer(
                text="Spred 0.5 ga muvaffaqiyatli o'zgartirildi ✅ ",
                show_alert=True
            )
            await call.message.answer(
                text="Savdo bot menyusi:",
                reply_markup=p2p_menyu
            )
            await call.message.delete()
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti, iltimos keyinroq urinib ko'ring!", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"✅✅✅✅✅✅✅\n\nBotda birjani UPDATE qilishda xatolik ketdi: {err}\n\n✅✅✅✅✅✅✅"
            )
    if malumotlar[1] == "15":
        try:
            db.update_birja(
                birja=1.5,
                user_id=call.from_user.id
            )
            await call.answer(
                text="Spred 1.5 ga muvaffaqiyatli o'zgartirildi ✅ ",
                show_alert=True
            )
            await call.message.answer(
                text="Savdo bot menyusi:",
                reply_markup=p2p_menyu
            )
            await call.message.delete()
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti, iltimos keyinroq urinib ko'ring!", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"✅✅✅✅✅✅✅\n\nBotda birjani UPDATE qilishda xatolik ketdi: {err}\n\n✅✅✅✅✅✅✅"
            )
    if malumotlar[1] == "30":
        try:
            db.update_birja(
                birja=3.0,
                user_id=call.from_user.id
            )

            await call.answer(
                text="Spred 3.0 ga muvaffaqiyatli o'zgartirildi ✅ ",
                show_alert=True
            )
            await call.message.answer(
                text="Savdo bot menyusi:",
                reply_markup=p2p_menyu
            )
            await call.message.delete()
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti, iltimos keyinroq urinib ko'ring!", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"✅✅✅✅✅✅✅\n\nBotda birjani UPDATE qilishda xatolik ketdi: {err}\n\n✅✅✅✅✅✅✅"
            )
    if malumotlar[1] == "50":
        try:
            db.update_birja(
                birja=5.0,
                user_id=call.from_user.id
            )
            await call.answer(
                text="Spred 5.0 ga muvaffaqiyatli o'zgartirildi ✅ ",
                show_alert=True
            )
            await call.message.answer(
                text="Savdo bot menyusi:",
                reply_markup=p2p_menyu
            )
            await call.message.delete()
        except Exception as err:
            await call.answer("Botda texnik ishlar olib borilayapti, iltimos keyinroq urinib ko'ring!", show_alert=True)
            await call.message.delete()
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"✅✅✅✅✅✅✅\n\nBotda birjani UPDATE qilishda xatolik ketdi: {err}\n\n✅✅✅✅✅✅✅"
            )


@dp.callback_query_handler(text="choose_birjas")
async def choose_birja_handler(call: types.CallbackQuery):
    if db.check_user_valyuta(call.from_user.id):
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )
    else:
        db.add_valyuta(
            user_id=call.from_user.id,
            Binance="True",
            HuobiGlobal="True",
            Bybit="True",
            OKX="True"
        )
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )


@dp.callback_query_handler(text_contains = "choose_birja:")
async def birja_choose_handler(call: types.CallbackQuery):
    malumotlar = call.data.rsplit(":")
    if malumotlar[1] == "binance":
        db.binance_update(
            Binance=malumotlar[2],
            user_id=call.from_user.id
        )
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )
    if malumotlar[1] == "huobiglobal":
        db.HuobiGlobal_update(
            HuobiGlobal=malumotlar[2],
            user_id=call.from_user.id
        )
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )
    if malumotlar[1] == "bybit":
        db.Bybit_update(
            Bybit=malumotlar[2],
            user_id=call.from_user.id
        )
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )
    if malumotlar[1] == "okx":
        db.OKX_update(
            OKX=malumotlar[2],
            user_id=call.from_user.id
        )
        await call.message.edit_text(
            text="Birjalarni tanlang:",
            reply_markup=choosebirjas(
                id_user=call.from_user.id
            )
        )


@dp.callback_query_handler(text = "about_birja")
async def about_birja_handler(call: types.CallbackQuery):
    await call.message.answer("Birjalardan kelgan signallarni qanday ishlatish!")


@dp.callback_query_handler(text = "cancel_birjas")
async def cancel_birjas_handler(call: types.CallbackQuery):
    await call.message.delete()

