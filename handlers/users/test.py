from aiogram import types
from loader import dp, bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.buttons import Javob
from keyboards.default.buttons import main_menu, leave_test_btn
from loader import db, dp, bot
from data.config import ADMINS


from states.states import Test


@dp.message_handler(text='📝 Test ishlash')
async def geo(message: types.Message):
    test = db.select_user_info(user_id=message.from_user.id)
    if test[-1] == 'True':
        await message.answer("Siz avval test yechgansiz!")
        await message.delete()
    else:
        db.update_test(test='True', user_id=message.from_user.id)
        text = """
⚠️⚠️⚠️
❗️ <b>Eslatib o'tamiz!</b>

<i>Sizga test yechish imkoniyati bir marta beriladi.
Agar siz test yechish mobaynida testdan chiqib ketsangiz qaytib yana
test yecha olmaysiz!</i>

⚠️ <i><b><u>E'TIBORLI BO'LING</u></b></i> ⭕️
    """
        await message.answer(text, reply_markup=leave_test_btn)
        await message.answer("Test Boshlandi! 🚀🚀🚀", reply_markup=leave_test_btn)
        savol1 = db.select_test(id=1)
        for test1 in savol1:
            await message.answer(text=f"1-Test:\n\n{test1[1]}\n\nA: {test1[2]}\nB: {test1[3]}\nC: {test1[4]}", reply_markup=Javob)
            await Test.Test1.set()


@dp.callback_query_handler(state=Test.Test1)
async def test1(call: types.CallbackQuery, state: FSMContext):
    test1 = call.data
    print(test1)
    await state.update_data({'Test1': test1})
    savol2 = db.select_test(id=2)
    for test2 in savol2:
        await call.message.edit_text(text=f"2-Test:\n\n{test2[1]}\n\nA: {test2[2]}\nB: {test2[3]}\nC: {test2[4]}", reply_markup=Javob)
        await Test.Test2.set()


@dp.callback_query_handler(state=Test.Test2)
async def test2(call: types.CallbackQuery, state: FSMContext):
    test2 = call.data
    await state.update_data({'Test2': test2})
    savol3 = db.select_test(id=3)
    for test3 in savol3:
        await call.message.edit_text(text=f"3-Test:\n\n{test3[1]}\n\nA: {test3[2]}\nB: {test3[3]}\nC: {test3[4]}", reply_markup=Javob)
        await Test.Test3.set()


@dp.callback_query_handler(state=Test.Test3)
async def test3(call: types.CallbackQuery, state: FSMContext):
    test3 = call.data
    await state.update_data({'Test3': test3})
    savol4 = db.select_test(id=4)
    for test4 in savol4:
        await call.message.edit_text(text=f"4-Test:\n\n{test4[1]}\n\nA: {test4[2]}\nB: {test4[3]}\nC: {test4[4]}", reply_markup=Javob)
        await Test.Test4.set()


@dp.callback_query_handler(state=Test.Test4)
async def test4(call: types.CallbackQuery, state: FSMContext):
    test4 = call.data
    await state.update_data({'Test4': test4})
    savol5 = db.select_test(id=5)
    for test5 in savol5:
        await call.message.edit_text(text=f"5-Test:\n\n{test5[1]}\n\nA: {test5[2]}\nB: {test5[3]}\nC: {test5[4]}", reply_markup=Javob)
        await Test.Test5.set()


@dp.callback_query_handler(state=Test.Test5)
async def test5(call: types.CallbackQuery, state: FSMContext):
    test5 = call.data
    await state.update_data({'Test5': test5})
    savol6 = db.select_test(id=6)
    for test6 in savol6:
        await call.message.edit_text(text=f"6-Test:\n\n{test6[1]}\n\nA: {test6[2]}\nB: {test6[3]}\nC: {test6[4]}", reply_markup=Javob)
        await Test.Test6.set()


@dp.callback_query_handler(state=Test.Test6)
async def test6(call: types.CallbackQuery, state: FSMContext):
    test6 = call.data
    await state.update_data({'Test6': test6})
    savol7 = db.select_test(id=7)
    for test7 in savol7:
        await call.message.edit_text(text=f"7-Test:\n\n{test7[1]}\n\nA: {test7[2]}\nB: {test7[3]}\nC: {test7[4]}", reply_markup=Javob)
        await Test.Test7.set()


@dp.callback_query_handler(state=Test.Test7)
async def test7(call: types.CallbackQuery, state: FSMContext):
    test7 = call.data
    await state.update_data({'Test7': test7})
    savol8 = db.select_test(id=8)
    for test8 in savol8:
        await call.message.edit_text(text=f"8-Test:\n\n{test8[1]}\n\nA: {test8[2]}\nB: {test8[3]}\nC: {test8[4]}", reply_markup=Javob)
        await Test.Test8.set()


@dp.callback_query_handler(state=Test.Test8)
async def test8(call: types.CallbackQuery, state: FSMContext):
    test8 = call.data
    await state.update_data({'Test8': test8})
    savol9 = db.select_test(id=9)
    for test9 in savol9:
        await call.message.edit_text(text=f"9-Test:\n\n{test9[1]}\n\nA: {test9[2]}\nB: {test9[3]}\nC: {test9[4]}", reply_markup=Javob)
        await Test.Test9.set()


@dp.callback_query_handler(state=Test.Test9)
async def test9(call: types.CallbackQuery, state: FSMContext):
    test9 = call.data
    await state.update_data({'Test9': test9})
    savol10 = db.select_test(id=10)
    for test10 in savol10:
        await call.message.edit_text(text=f"10-Test:\n\n{test10[1]}\n\nA: {test10[2]}\nB: {test10[3]}\nC: {test10[4]}", reply_markup=Javob)
        await Test.Test10.set()


@dp.callback_query_handler(state=Test.Test10)
async def test10(call: types.CallbackQuery, state: FSMContext):
    test10 = call.data
    await state.update_data({'Test10': test10})
    await call.message.delete()
    javob = await state.get_data()
    ball = 0
    Test1 = javob.get('Test1')
    savol1 = db.select_test(id=1)
    if Test1 == savol1[0][5]:
        ball += 1
    else:
        pass
    Test2 = javob.get('Test2')
    savol2 = db.select_test(id=2)
    if Test2 == savol2[0][5]:
        ball += 1
    else:
        pass
    Test3 = javob.get('Test3')
    savol3 = db.select_test(id=3)
    if Test3 == savol3[0][5]:
        ball += 1
    else:
        pass
    Test4 = javob.get('Test4')
    savol4 = db.select_test(id=4)
    if Test4 == savol4[0][5]:
        ball += 1
    else:
        pass
    Test5 = javob.get('Test5')
    savol5 = db.select_test(id=5)
    if Test5 == savol5[0][5]:
        ball += 1
    else:
        pass
    Test6 = javob.get('Test6')
    savol6 = db.select_test(id=6)
    if Test6 == savol6[0][5]:
        ball += 1
    else:
        pass
    Test7 = javob.get('Test7')
    savol7 = db.select_test(id=7)
    if Test7 == savol7[0][5]:
        ball += 1
    else:
        pass
    Test8 = javob.get('Test8')
    savol8 = db.select_test(id=8)
    if Test8 == savol8[0][5]:
        ball += 1
    else:
        pass
    Test9 = javob.get('Test9')
    savol9 = db.select_test(id=9)
    if Test9 == savol9[0][5]:
        ball += 1
    else:
        pass
    Test10 = javob.get('Test10')
    await state.finish()
    savol10 = db.select_test(id=10)
    if Test10 == savol10[0][5]:
        ball += 1
    else:
        pass
#   u_ball = db.check_user(user_id=call.from_user.id)
    await bot.send_message(chat_id=call.from_user.id, text=f"<b>Test yakunlandi\n\nTo'g'ri javoblar soni: {ball} ta</b>\nBilimingizni sinab ko'rganingiz uchun rahmat. ", reply_markup=main_menu)
    malumotlar = db.select_user_info(user_id=call.from_user.id)
    text = f"🎉 Yangi test topshirildi.\n\n"
    text += f"🆔 <b>User-ID</b>: <code>{malumotlar[1]}</code>\n"
    text += f"📄 <b>Username:</b> <i>@{malumotlar[2]}</i>\n"
    text += f"📖 <b>Fullname:</b> <i>{malumotlar[3]}</i>\n"
    text += f"☎️ <b>Telefon:</b> <i>{malumotlar[4]}</i>\n"
    text += f"💠 <b>Test natijasi: </b> <i>10 ta savoldan {ball} ta to'g'ri javob!</i>"
    await bot.send_message(
        chat_id=-1001971452921,
        text=text
    )
    await state.finish()
