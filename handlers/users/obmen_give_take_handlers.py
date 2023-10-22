from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from datetime import datetime
from loader import dp, db
from data.config import ADMINS
from states.berishOlishSum import BerSum, OlSum
from handlers.users.obmen_change_handlers import valutas
from keyboards.default.buttons import main_menu
from keyboards.inline.pay import payOrCancel, payedOrCancel
from keyboards.inline.cancel import Cancel
from keyboards.inline.adminResult import success_or_fail
from utils.db_api.dbxl import getWalletData, get_data, getTransferId, addOperation

pul_birligi = {"uzcard": "SO'M", "humo": "SO'M", "usdt": "USDT", }

kassaWallet = {"uzcard": "8600 0417 7912 8082",
               "humo": "9860 6004 3836 1559", "usdt": "88842771", }


# Olishni kiritishga alohida limit sharti yozish kerak
def llimiter(type, givtake='choose_berish'):
    if givtake == 'choosen_berish':
        if pul_birligi[type] == "SO'M":
            min_sum = 110000
            max_sum = 10000000
        elif pul_birligi[type] == "USDT":
            min_sum = 110000
            max_sum = 10000000

        text = (f"Berish miqdorini {pul_birligi[type]} birligida kiriting:",
                f"Minimal: <code>{min_sum}</code>",
                f"Maksimal: <code>{max_sum}</code>")

    elif givtake == 'choosen_olish':
        if pul_birligi[type] == "SO'M":
            min_sum = 110000
            max_sum = 10000000
        elif pul_birligi[type] == "USDT":
            min_sum = 110000
            max_sum = 10000000
        text = (f"Berish miqdorini {pul_birligi[type]} birligida kiriting:",
                f"Minimal: <code>{min_sum}</code>",
                f"Maksimal: <code>{max_sum}</code>")

    return text, min_sum, max_sum


@dp.callback_query_handler(text='choosen_berish')
async def berKirit(call: CallbackQuery, state: FSMContext):
    datas = await state.get_data()      # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    berish = datas.get(f"ber_{call.from_user.id}")
    text = llimiter(berish, 'choosen_berish')[0]
    await call.message.answer("\n".join(text), reply_markup=Cancel)
    await call.message.delete()
    await BerSum.berish_sum.set()


@dp.callback_query_handler(text='choosen_olish')
async def olKirit(call: CallbackQuery, state: FSMContext):
    # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    datas = await state.get_data()
    olish = datas.get(f"ol_{call.from_user.id}")
    text = llimiter(olish, 'choosen_olish')[0]
    await call.message.answer("\n".join(text), reply_markup=Cancel)
    await call.message.delete()
    await OlSum.olish_sum.set()


@dp.message_handler(state=BerSum.berish_sum)
async def viewSumma(message: Message, state: FSMContext):

    datas = await state.get_data()      # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    berish = datas.get(f"ber_{message.from_user.id}")
    olish = datas.get(f"ol_{message.from_user.id}")

    text = llimiter(berish, 'choosen_berish')[0]
    limit_min = llimiter(berish, 'choosen_berish')[1]
    print(f"LIMIT-MIN => {limit_min}")
    limit_max = llimiter(berish, 'choosen_berish')[2]
    print(f"LIMIT-MAX => {limit_max}")

    try:
        print(f"{int(message.text) >= limit_min and {int(message.text) <= limit_max}}")
        if int(message.text) >= limit_min and int(message.text) <= limit_max:
            kurs = int(db.get_kurs(id=1)[1])
            if pul_birligi[berish] == "SO'M" and pul_birligi[olish] == "USDT":
                olish_sum = round(int(message.text) / kurs, 2)

            elif pul_birligi[berish] == 'USDT' and pul_birligi[olish] == "SO'M":
                olish_sum = round(int(message.text) * kurs, 2)

            await state.update_data(
                {'userdan_sum': f"{message.text} {pul_birligi[berish]}",
                 'userga_sum': f"{olish_sum} {pul_birligi[olish]}"}
            )

            text = ("🔀 <b>Almashuv</b>",
                    f"🆔 ID: <code>{getTransferId()}</code>",
                    f"⬆️ Berish: {message.text} {pul_birligi[berish]}",
                    f"⬇️ Olish: {olish_sum} {pul_birligi[olish]}",
                    f"🔹 <b>{valutas[berish]}: {getWalletData(message.from_user.id, berish)}</b>",
                    f"♦️ <b>{valutas[olish]}: {getWalletData(message.from_user.id, olish)}</b>")
            await message.answer("\n".join(text), reply_markup=payOrCancel)

            await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
        else:
            i = 0/0     # Xatolik keltirib chiqarish uchun

    except:
        await message.answer("\n".join(text), reply_markup=Cancel)


@dp.message_handler(state=OlSum.olish_sum)
async def viewSumma(message: Message, state: FSMContext):
    datas = await state.get_data()      # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    berish = datas.get(f"ber_{message.from_user.id}")
    olish = datas.get(f"ol_{message.from_user.id}")

    text = llimiter(olish, 'choosen_olish')[0]
    limit_min = llimiter(olish, 'choosen_olish')[1]
    limit_max = llimiter(olish, 'choosen_olish')[2]

    try:
        if int(message.text) >= limit_min and int(message.text) <= limit_max:
            kurs = int(db.get_kurs(id=1)[2])
            if pul_birligi[berish] == "SO'M" and pul_birligi[olish] == "USTD":
                # kurs = int(db.get_kurs(id=1)[2])
                berish_sum = round(int(message.text) * kurs, 2)

            elif pul_birligi[berish] == "USDT" and pul_birligi[olish] == "SO'M":
                # kurs = int(db.get_kurs(id=1)[2])
                berish_sum = round(int(message.text) * kurs, 2)

            elif pul_birligi[berish] == "SO'M" and pul_birligi[olish] == "USDT":
                # kurs = int(db.get_kurs(id=1)[2])
                berish_sum = round(int(message.text) / kurs, 2)

            await state.update_data(
                {'userdan_sum': f"{berish_sum} {pul_birligi[berish]}",
                 'userga_sum': f"{message.text} {pul_birligi[olish]}"}
            )

            text = ("🔀 <b>Almashuv</b>",
                    f"🆔 ID: <code>{getTransferId()}</code>",
                    f"⬆️ Berish: {berish_sum} {pul_birligi[berish]}",
                    f"⬇️ Olish: {message.text} {pul_birligi[olish]}",
                    f"🔹 <b>{valutas[berish]}: {getWalletData(message.from_user.id, berish)}</b>",
                    f"♦️ <b>{valutas[olish]}: {getWalletData(message.from_user.id, olish)}</b>")
            await message.answer("\n".join(text), reply_markup=payOrCancel)

            await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
        else:
            i = 0/0     # Xatolik keltirib chiqarish uchun

    except:
        await message.answer("\n".join(text), reply_markup=Cancel)


@dp.callback_query_handler(text='pay', state=[BerSum, OlSum])
async def pay(call: CallbackQuery, state: FSMContext):
    # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    datas = await state.get_data()
    berish = datas.get(f"ber_{call.from_user.id}")
    userdan_sum = datas.get(f"userdan_sum")

    await call.message.answer(kassaWallet[berish])
    await call.message.answer(f"👆Ko'chirib olish uchun \n\nAlmashuvingiz muvaffaqiyatli bajarilishi uchun quyidagi harakatlarni amalga oshiring:\n\n1) Pastda ko'rsatilgan to'lov miqdorni  -  {kassaWallet[berish]}  raqamiga o'tkazing;\n\n2) «To'lov qildim ✅» tugmasini bosing; \n3) Operator tomonidan almashuv tasdiqlanishini kuting.\n\n\n <b>To'lov miqdori: {userdan_sum}</b> \n\nUshbu almashuv operator tomonidan navbati bilan amalga oshiriladi va 2 daqiqadan 30 daqiqagacha davom etadi.", reply_markup=payedOrCancel)
    await call.message.delete()


@dp.callback_query_handler(text='payed', state=[BerSum, OlSum])
async def pay(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    # delete WalletNumni o'chiradi
    await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
    await dp.bot.send_message(
        chat_id=call.from_user.id,
        text="To'lov qilganingiz haqidagi screenshotni yuboring.",
        reply_markup=Cancel
    )


@dp.message_handler(content_types=types.ContentType.PHOTO, state=[BerSum, OlSum])
async def screenshot_handler(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    # Vaqtinchalik ma'lumotlarni qayta o'qiymiz
    datas = await state.get_data()
    berish = datas.get(f"ber_{message.from_user.id}")
    olish = datas.get(f"ol_{message.from_user.id}")
    userdan_sum = datas.get(f"userdan_sum")
    userga_sum = datas.get(f"userga_sum")

    await state.finish()            # Userni state'dan chiqaramiz

    await message.answer(
        text=f"<b>Almashuv ID: {getTransferId()} </b>\nBuyurtmangiz operatorga yuborildi, iltimos tasdiqlanishini kuting!", reply_markup=main_menu)

    text = ("<b>Almashuv</b>",
            f"🆔 r-ID: {message.from_user.id}",
            f"👤 User: {message.from_user.full_name}",
            f"📝 Username: @{message.from_user.username}",
            f"🔰 To'lov <b>ID</b>: {getTransferId()}",
            f"🔀: {valutas[berish]} --> {valutas[olish]}",
            f"🔼User {valutas[berish]} Num: {getWalletData(message.from_user.id, berish)}",
            f"🔽 User {valutas[olish]} Num: {getWalletData(message.from_user.id, olish)}",
            f"💰 Userdan summa: {userdan_sum}",
            f"💵 Userga summa: {userga_sum}"
            )

    await dp.bot.send_photo(-1001910192172, photo_id, "\n".join(text), reply_markup=success_or_fail(user_id=message.from_user.id))
    try:
        db.add_transfer(
            user_id=message.from_user.id,
            exchange=f"{valutas[berish]} --> {valutas[olish]}",
            updated_time=datetime.now(),
            status="W",
            summa=f"{userdan_sum}"
        )
    except Exception as err:
        print(err)
    # Bazaga qo'shish
    addOperation(valutas[berish],
                 valutas[olish],
                 getWalletData(message.from_user.id, berish),
                 getWalletData(message.from_user.id, olish),
                 f"{userdan_sum}",
                 f"{userga_sum}",
                 message.from_user.full_name,
                 message.from_user.username,
                 message.from_user.id
                 )
