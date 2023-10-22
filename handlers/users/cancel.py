from aiogram import types
from loader import db, dp, bot
from keyboards.default.buttons import *
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start', 'cancel'], state="*")
@dp.message_handler(text="🏠 Bosh menyu", state="*")
@dp.message_handler(text="🔙 Bekor qilish", state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=second_menu)
        await state.finish()
    if datas[0] == "False":
        await state.finish()
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
    if datas[0] == "Waiting":
        await state.finish()
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)


@dp.callback_query_handler(text='cancel', state='*')
async def choose1(call: types.CallbackQuery, state: FSMContext):
    datas = db.get_user_subs(call.from_user.id)
    if datas[0] == "True":
        await call.message.answer("🏠 Siz bosh menyudasiz.", reply_markup=second_menu)
        await state.finish()
        await call.message.delete()
    if datas[0] == "False":
        await state.finish()
        await call.message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
        await call.message.delete()
    if datas[0] == "Waiting":
        await state.finish()
        await call.message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
        await call.message.delete()


@dp.message_handler(text="🔙 Testdan chiqish", state="*")
async def leave_test(message: types.Message, state: FSMContext):
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=second_menu)
        await state.finish()
    if datas[0] == "False":
        await state.finish()
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
    if datas[0] == "Waiting":
        await state.finish()
        await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=main_menu)
