from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import date, timedelta
from aiogram.dispatcher import FSMContext
import re
from utils.misc.subscription import check_status
from loader import dp, db, bot
from data.config import ADMINS, DEVELOPER
from keyboards.default.buttons import main_menu, contact_button, second_menu
from states.states import UserRegisterState
from keyboards.inline.buttons import *
from keyboards.inline.subs import SubscChanBtn

text_sub = "Botdan to'laqonli foydalanish uchun quyidagi kanallarga a’zo bo’ling. Keyin “<b>✅ A’zo bo’ldim</b>” tugmasini bosing."


# Start komandasi uchun handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if await check_status(user_id):
        if db.check_user(user_id=message.from_user.id):
            malumot = db.check_subscription(user_id=message.from_user.id)[0]
            if malumot == "True":
                await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=second_menu)
            if malumot == "Waiting":
                await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main_menu)
            if malumot == "False":
                await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main_menu)
        else:
            try:
                invite = message.get_args()
                print(invite)
                if invite:
                    try:
                        await bot.send_message(invite,
                                               f'🎉 Sizning havolangiz orqali yangi a\'zo {message.from_user.get_mention()} botga obuna bo\'ldi!')
                    except:
                        pass
                    raqam = db.get_userbalans(user_id=invite)[0]
                    try:
                        hisob = float(raqam)+float(0.3)
                    except:
                        pass
                    try:
                        db.update_balans(balans=hisob, user_id=invite)
                    except:
                        pass
                else:
                    invite = 0
                today = date.today()
                six_months = timedelta(days=30*6)
                future_date = today + six_months
                future_date_formatted = future_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
                db.add_user(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                    status="User",
                    linked_id=invite,
                    balans="0",
                    subscription="False",
                    subscription_off=future_date_formatted
                )
                await message.answer(f"Salom, {message.from_user.full_name}!\n<i>Ism va familiyangizni kiriting: </i>")
                await UserRegisterState.fullname.set()
            except Exception as err:
                await bot.send_message(chat_id=DEVELOPER, text=f"Error ERRROOOOORRRR: {err}")
                await message.answer("Botda texnik ishlar olib borilayapti iltimos, biroz vaqtdan keyin urinib ko'ring...")
    else:
        if db.check_user(message.from_user.id):
            pass
        else:
            invite = message.get_args()
            if invite:
                try:
                    await bot.send_message(invite,
                                           f'🎉 Sizning havolangiz orqali yangi a\'zo {message.from_user.full_name} botga obuna bo\'ldi!')
                except Exception as err:
                    print(err)
                try:
                    hisob = float(db.get_userbalans(
                        user_id=invite)[0])+float(0.3)
                    db.update_balans(balans=hisob, user_id=invite)
                except Exception as err:
                    print(err)
        await message.answer(text=text_sub, reply_markup=await SubscChanBtn(message.from_user.id))


@dp.callback_query_handler(text="check_subsciption")
async def bot_start(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except:
        pass
    user_id = call.from_user.id
    if await check_status(user_id):
        if db.check_user(user_id=call.from_user.id):
            await call.message.answer(f"Salom, {call.from_user.full_name}!", reply_markup=main_menu)
            try:
                await call.message.delete()
            except:
                pass
        else:
            try:
                await call.message.answer(f"Salom, {call.from_user.full_name}!\n<i>Ism va familiyangizni kiriting: </i>")
                await call.message.delete()
                await UserRegisterState.fullname.set()
            except Exception as err:
                pass

    else:
        await call.message.answer(text="""❌ Kanalga aʼzo boʼlmadingiz!
Botdan toʼliq foydalanish uchun koʼrsatilgan barcha kanallarga aʼzo boʼling!
Keyin “<b>A’zo bo’ldim</b>” tugmasini bosing.""",
                                  reply_markup=await SubscChanBtn(user_id))
    await call.answer(cache_time=1)


@dp.message_handler(state=UserRegisterState.fullname)
async def fullname_handler(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data({
        "fullname": text
    })
    await message.reply("<i>Telefon raqamingiz yuboring:</i>", reply_markup=contact_button)
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.phone, content_types=types.ContentTypes.CONTACT)
async def contact_handler(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data({
        "phone": contact
    })
    datas = await state.get_data()
    text = "<b>⚙️ Malumotlaringiz to'g'rimi? 👇</b>\n\n"
    text += f"<i>👤 Ism va familiya:</i> <b>{datas['fullname']}</b>\n"
    text += f"<i>📱 Telefon raqam: </i><b>{contact}</b>"
    await message.answer(text=text, reply_markup=check_datas_user)
    await UserRegisterState.next()


@dp.callback_query_handler(state=UserRegisterState.check)
async def check_user_handler(call: types.CallbackQuery, state: FSMContext):
    text = call.data
    datas = await state.get_data()
    if text == "yes_right":
        db.add_user_datas(
            user_fullname=datas['fullname'],
            phone=datas['phone'],
            user_id=call.from_user.id,
        )
        matn = f"🎉 Yangi foydalanuvchi. {call.from_user.get_mention()}\n"
        matn += f"🆔 <i>ID:</i> <code>{call.from_user.id}</code>\n"
        matn += f"📛 <i>Username:</i> <b>@{call.from_user.username}</b>\n"
        matn += f"📝 <i>Fullname:</i> <b>{datas['fullname']}</b>\n"
        matn += f"☎️ <i>Phone number:</i> <code>{datas['phone']}</code>\n\n"
        matn += f"📊 Bazada {db.count_users()[0]} ta foydalanuvchi mavjud."
        await state.finish()
        await call.message.answer("<b>Botdan to'laqonli foydalanish uchun obunani sotib oling.</b>", reply_markup=main_menu)
        for i in ADMINS:
            await bot.send_message(chat_id=i, text=matn)
        await call.message.delete()
    else:
        await call.message.answer("Qaytadan ism familiyangizni kiriting: ")
        await state.reset_data()
        await UserRegisterState.fullname.set()
        await call.message.delete()
