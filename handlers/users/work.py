from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db, bot, dp
from keyboards.inline.buttons import *
from keyboards.default.buttons import *
from states.states import ConnectUs, SendResultState
from data.config import ADMINS

# @dp.message_handler(content_types=types.ContentTypes.PHOTO)
# async def send_file_id(message: types.Message):
#     await message.answer(message.photo[-1].file_id)


@dp.message_handler(text="👤 Biz haqimizda")
async def about_us(message: types.Message):
    text = """
✋🏻Assalomaleykum Hurmatli Bo'lajak Treyder botimizga tashrif buyurganingizdan xursandmiz 😊 biz sizni daromadingizni oshirish maqsadida bu botni tashkil qildik.

👨‍💻Bizning ijtimoiy tarmoqlarimiz 👇

▪️Telegram - https://t.me/+sVn66CXL5Eg0YmY6

▪️Instagram - https://instagram.com/mk_samandar

▪️Tik Tok - https://www.tiktok.com/@mk.binance

▪️YouTube - https://youtube.com/@MkSamandar

▪️Saytimiz - Mkbinance.com
    """
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer(text, reply_markup=second_menu)
    if datas[0] == "False":
        await message.answer(text, reply_markup=main_menu)
    if datas[0] == "Waiting":
        await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text="🧑🏻‍💻 Operator bilan bog'lanish")
async def about_us(message: types.Message):
    await message.answer("✋🏻Assalomaleykum qanday savollaringiz va takliflaringiz bor biz sizni eshitamiz batafsil yozib qoldiring 👇", reply_markup=back_button)
    await ConnectUs.text.set()


@dp.message_handler(state=ConnectUs.text)
async def send_admin_handler(message: types.Message, state: FSMContext):
    text = message.text
    if text == "🔙 Bekor qilish":
        datas = db.get_user_subs(user_id=message.from_user.id)
        if datas[0] == "True":
            await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=second_menu)
            await state.finish()
        if datas[0] == "False":
            await state.finish()
            await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
        if datas[0] == "Waiting":
            await state.finish()
            await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
    else:
        await bot.send_message(
            chat_id=ADMINS[0],
            text=text,
            reply_markup=answer_question(user_id=message.from_user.id)
        )
        malumot = db.check_subscription(user_id=message.from_user.id)[0]
        if malumot == "True":
            await message.answer("Savolingiz operatorga yuborildi, iltimos operator javobini kuting. ⏳", reply_markup=second_menu)
        if malumot == "False":
            await message.answer("Savolingiz operatorga yuborildi, iltimos operator javobini kuting. ⏳", reply_markup=main_menu)
        if malumot == "Waiting":
            await message.answer("Savolingiz operatorga yuborildi, iltimos operator javobini kuting. ⏳", reply_markup=main_menu)
        await state.finish()


@dp.message_handler(text="📎 Referal bo'limi")
async def referal_part(message: types.Message):
    user_suu = await bot.get_me()
    text = f"""
✅ <b>«{user_suu.full_name}»</b>

🎈 <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> do'stingizdan unikal havola-taklifnoma.

👇 Boshlash uchun bosing:
https://t.me/{user_suu.username}?start={message.from_user.id}
    """
    rasm = types.InputFile(path_or_bytesio="photos/image.jpg")
    await message.reply(text="<b>Quyidagi havolani doʻstlaringizga tarqating va har bitta kirgan do'stingiz uchun 0.3$ ishlab oling! 👇</b>")
    await message.answer_photo(photo=rasm, caption=text, reply_markup=share_btn(user_id=message.from_user.id))


@dp.message_handler(text="📶 Signal haqida ma'lumot")
async def about_signal(message: types.Message):
    text = """
🔸Assalomaleykum hurmatli Treyder botimiz orqaliy siz kunlik 1-5 tagacha Binance uchun SPOT/FYUCHERS bo'limlariga savdo qilishingiz uchun Signall olishingiz mumkin 

🔸Albatta sotib olingan signallaringiz daromadga sizni olib chiqadi faqatgina to'g'ri invesitsiya va savdoni to'g'ri qila olsangiz bass 

🔸Signall sotib olishimiz uchun nima qilishimiz kerak ? va Signall kanal qancha deganlar uchun Signall sotib olish degan KNOPKANI bosangiz narxlari chiqadi signall sotib olganingizdan so'ng sizga bonus tariqasida analiz video darsliklari bepul beriladi.

🔸Agar siz signall sotib olishda ikkilanayotgan bo'lsangiz Signall natijalarini kanal orqaliy ko'rishingiz mumkin bu bo'lib botimizda bor Agar pulik obunani sotib olishga tayyor bo'lsangiz ketik...🚀
    """
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer(text, reply_markup=second_menu)
    if datas[0] == "False":
        await message.answer(text, reply_markup=main_menu)
    if datas[0] == "Waiting":
        await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text="📊 Natijalar")
async def reulst(message: types.Message):
    await message.answer("Tanglang 👇", reply_markup=results_part)


@dp.message_handler(text="📊 Natijalarni ko'rish")
async def show_results(message: types.Message):
    text = """
<b>
🤖Botimizning foydalanuvchilari qilgan natijalarini 
bu kanaldan ko'rishingiz mumkin - https://t.me/+gy1EAqhcOBhjZmMy
</b>
"""
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer(text, reply_markup=second_menu)
    if datas[0] == "False":
        await message.answer(text, reply_markup=main_menu)
    if datas[0] == "Waiting":
        await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text="📤 Natijalarni yuborish")
async def send_results(message: types.Message):
    await message.answer("❗️Hurmatli Treyder Botimizdagi signallar orqaliy natija qilgan bo'lsangiz screnshotlaringizni jonatishingiz mumkin ☺️", reply_markup=back_button)
    await SendResultState.result.set()


@dp.message_handler(state=SendResultState.result, content_types=types.ContentTypes.PHOTO)
async def send_admin_result(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data({
        "result": photo
    })
    await SendResultState.next()
    await message.reply("<i>📝 O'zingiz va natijangiz haqida yozing</i>")


@dp.message_handler(state=SendResultState.text, content_types=types.ContentTypes.TEXT)
async def about_result(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    rasm = data['result']
    await bot.send_photo(
        chat_id=ADMINS[0],
        photo=rasm,
        caption=text
    )
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer("Adminga yuborildi. ✅", reply_markup=second_menu)
        await state.finish()
    if datas[0] == "False":
        await state.finish()
        await message.answer("Adminga yuborildi. ✅", reply_markup=main_menu)
    if datas[0] == "Waiting":
        await state.finish()
        await message.answer("Adminga yuborildi. ✅", reply_markup=main_menu)


@dp.message_handler(text="📌 Qanday savdo qilish kerak?")
async def savdoni_qanday_handler(message: types.Message):
    await message.answer_document(document="https://t.me/ooooooooooo456/2")
    await message.answer_document(document="https://t.me/ooooooooooo456/3")
