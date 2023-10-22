from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.buttons import *
from keyboards.default.buttons import *
from aiogram.dispatcher import FSMContext
from states.states import AdminSendState, OperatorState


@dp.message_handler(text="📶 Signal sotib olish")
async def buy_signal(message: types.Message):
    await message.answer("Tanlang 👇", reply_markup=third_part)


@dp.message_handler(text="♻️ Obunani sotib olish")
async def subscription_text(message: types.Message):
    status = db.get_user_subs(user_id=message.from_user.id)[0]
    if status == "Waiting":
        await message.answer("<b>Siz sotib olgansiz, javobingiz kutilmoqda!\nIltimos, admin javobini kuting.</b>")
    if status == "True":
        await message.answer("Siz, avval sotib olgansiz!\nObuna muddati tugaganidan keyin yana qaytadan sotib olishingiz mumkin bo'ladi.")
    if status == "False":
        await message.answer("Qaysi usulda to'lovni amalga oshirmoqchisiz? 👇", reply_markup=payment_buttons())


@dp.callback_query_handler(text_contains="pay:")
async def payment_handler(call: types.CallbackQuery):
    tools = call.data.rsplit(":")
    print(tools)
    await call.message.answer("Obunani qancha muddatga sotib olmoqchisiz?", reply_markup=date_subscription(
        payment_method=tools[1]
    ))
    await call.message.delete()


@dp.callback_query_handler(text_contains="subscription_date:")
async def subs_date_handler(call: types.CallbackQuery):
    tools = call.data.rsplit(":")
    payments_datas = db.get_payment(name=tools[2])
    prices_datas = db.get_price(id=tools[1])
    text = f"<i>⚙️ To'lov usuli</i>: <b>{tools[2].upper()}</b>\n\n"
    text += f"<i>📅 Obuna muddati: <b>{prices_datas[1]}</b></i>\n\n"
    try:
        db.update_subs_month(
            subs_month=tools[1],
            user_id=call.from_user.id
        )
    except:
        pass
    text += f"<i>💰 Narx👇\n<b>{prices_datas[2]} $</b>\n<b>{prices_datas[3]} So'm</b>\n<b>{prices_datas[4]} Rubl</b></i>\n\n"
    text += f"<b>{tools[2].upper()}</b> <i>orqali ushbu kartaga to'lov qiling 👇\n<code>{payments_datas[3]}</code></i>"
    await call.message.answer("""
🤖Robotimiz haqida Qisqacha Malumolar Tolov qilishdan Oldin O'qib Chiqing Iltmos ❗️

▪️Robotimizning Asosiy vazifalari CopyTrading, Kriptovalyutalarga Signallar, Fond Birjasiga Signallar, P2P uchun Svyaskalar shu bo'limlar bizda asosiy Instrument sifatida ishlatishingizga yordam beradigan bo'limlar hisoblanadi.

▪️COPYTRADING bo'limi TOP Binancedagi Treydirlarning ochgan savdolarini ko'rib tanlab takrorlashingiz mumkin bo'ladigan bo'lim ✅

▪️Kriptovalyutaga Signall bo'limi , Kriptovalyutalarga Signallar beriladi Fatures bo'limiga Va SPOT bo'limiga 

▪️Fond Birjasiga Signallar bo'limi, Bu bo'limda ham fond birjasiga signallarni olishingiz mumkin 

▪️P2P uchun Svyaskalar bu bo'limda siz Binance va Boshqa birjalar ichida va Birjalar aro savdoni amalga oshirasiz Robot Svyaska beradi. 

Robotimizda Qilingan Ochgan Savdoyingiz uchun hech kim Javob bermaydi. Robotga Qilingan Tolov hech qanday Xolatlarda Ham Qaytarib berilmaydi (Hech qanday baxonalarsiz) 

❗️Eslatma Agar siz robotning husiyatlari bilan tanishib chiqan bo'lsangiz tolov qilishga tayyor bo'lsangiz unda olg'a 😊👇
    """)
    await call.message.answer_photo(photo=f"{payments_datas[2]}", caption=text, reply_markup=send_admin_screenshot)
    await call.message.delete()


@dp.callback_query_handler(text="send_admin_screenshot")
async def send_admin(call: types.CallbackQuery):
    await call.message.answer("🖼 Adminga yuborilishi kerak bo'lgan screenshotni kiriting:", reply_markup=types.ForceReply())
    await AdminSendState.photo.set()
    await call.message.delete_reply_markup()


@dp.message_handler(state=AdminSendState.photo, content_types=types.ContentTypes.PHOTO)
async def send_photo(message: types.Message, state: FSMContext):
    try:

        await bot.forward_message(chat_id=ADMINS[0],
                                  from_chat_id=message.chat.id,
                                  message_id=message.message_id)
        subs_month = int(db.get_subs_month(
            user_id=message.from_user.id
        )[0])
        month_datas = db.get_month(
            id=subs_month
        )
        text = f"User ID: <code>{message.from_user.id}</code>\n"
        text += f"Username: @{message.from_user.username}\n"
        text += f"Obuna muddati: <b>{month_datas[1]}</b>\n"
        text += f"To'lanishi kerak: <code>{month_datas[2]} $</code>"
        await bot.send_message(
            chat_id=ADMINS[0],
            text=text,
            reply_markup=admin_check_buttons(user_id=message.from_user.id)
        )
    except Exception as err:
        print(err)
    await state.finish()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id
        )
        await message.answer("Yuborildi ✅\nIltimos admin javobini kuting.⏰")
        db.update_user_subs(
            subscription="Waiting",
            user_id=message.from_user.id
        )
    except:
        pass


@dp.callback_query_handler(text_contains="answerquestion:")
async def answer_operator(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.replace("answerquestion:", "")
    await OperatorState.user_id.set()
    await state.update_data({"user_id": user_id})
    await OperatorState.next()
    await call.message.answer("Javobni kiriting: ")
    await call.message.delete_reply_markup()


@dp.message_handler(state=OperatorState.answer, content_types=types.ContentTypes.ANY)
async def operator_answer(message: types.Message, state: FSMContext):
    text = message.text
    datas = await state.get_data()
    try:
        await bot.send_message(
            chat_id=datas['user_id'],
            text=text
        )
    except:
        pass
    await message.answer("Yuborildi ✅", reply_markup=second_menu)
    await state.finish()


@dp.message_handler(text="💴 Referal balans")
async def refer_balans(message: types.Message):
    hisob = db.get_userbalans(message.from_user.id)[0]
    if hisob == None:
        pul = 0
    else:
        pul = round(hisob, 1)
    text = f"💸<i>Sizning hisobingiz:</i> <b>{pul} $</b>\n"
    text += f"👥<i>Taklif qilgan do'stlaringiz soni:</i> <code>{len(db.get_invited(linked_id=message.from_user.id))}</code>\n"
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer(text, reply_markup=second_menu)
    if datas[0] == "False":
        await message.answer(text, reply_markup=main_menu)
    if datas[0] == "Waiting":
        await message.answer(text, reply_markup=main_menu)
