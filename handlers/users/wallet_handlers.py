from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils.db_api.dbxl import addWallet_db, clearWallets
from keyboards.default.buttons import main_menu, second_menu
from keyboards.default.wallet_keyboard import addWallet
from states.mapMenu import Map
from states.mapWallet import EditWallet


@dp.message_handler(text='🔙Asosiy menyu', state="*")   # Asosiy menuga qaytish
async def change(message: types.Message, state: FSMContext):
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.answer("Asosiy menyu", reply_markup=second_menu)
    if datas[0] == "False":
        await message.answer("Asosiy menyu", reply_markup=main_menu)
    if datas[0] == "Waiting":
        await message.answer("Asosiy menyu", reply_markup=main_menu)
    await state.finish()


@dp.message_handler(text=['➕UZCARD', '➕HUMO', '➕USDT'], state="*")
async def change(message: types.Message, state: FSMContext):
    retext = " raqamlarini kiriting.\nBo'sh joylarsiz, boshqa belgilarsiz"
    if message.text == '➕UZCARD':
        text = 'UZCARD kartangiz'+retext
        await EditWallet.EditUzcard.set()

    elif message.text == '➕HUMO':
        text = 'HUMO kartangiz'+retext
        await EditWallet.EditHumo.set()

    elif message.text == '➕USDT':
        text = 'USDT hamyoningiz raqamini kiriting.\n\nFormat: 426968609'
        await EditWallet.EditQiwi.set()
    await message.reply(text)


# Add UZCARD
@dp.message_handler(state=EditWallet.EditUzcard)
async def change(message: types.Message, state: FSMContext):
    card_num = message.text

    try:
        card_num = int(card_num)
    except:
        card_num = 'not num'

    if type(card_num) == int and len(message.text) == 16:
        addWallet_db(message, 'G')
        await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
        await message.answer(f"{message.text} kartangiz yaroqlik muddatini kiriting\n\nFormat: 01/23 yoki 0123")
        await message.answer("Karta muvaffaqqiyatli qo'shildi", reply_markup=addWallet)
        await Map.hamyonlar.set()

    elif card_num == 'not num' or len(message.text) != 16:
        await message.answer("UZCARD kartangiz ustidagi 16 talik raqamni kiriting!")


# @dp.message_handler(state = EditWallet.EditUzcardDate)
# async def change(message: types.Message, state:FSMContext):
#     if len(message.text) == 5:
#         await message.answer("Karta muvaffaqqiyatli qo'shildi", reply_markup = addWallet)
#         addWallet_db(message, 'H')
#         await Map.hamyonlar.set()

#     elif len(message.text) == 4:
#         uzcard_date = message.text[:2] + '/' + message.text[2:]
#         addWallet_db(message, 'H')
#         await message.answer("Karta muvaffaqqiyatli qo'shildi", reply_markup=addWallet)
#         await Map.hamyonlar.set()

#     else:
#         await message.answer("Noto'gri format kiritdingiz!\n\nFormat: 01/23 yoki 0123 kabi kiriting")


# Add HUMO
@dp.message_handler(state=EditWallet.EditHumo)
async def change(message: types.Message, state: FSMContext):
    card_num = message.text

    try:
        card_num = int(card_num)
    except:
        card_num = 'not num'

    if type(card_num) == int and len(message.text) == 16:
        addWallet_db(message, 'I')
        await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
        await message.answer("Karta muvaffaqqiyatli qo'shildi✅", reply_markup=addWallet)
        await Map.hamyonlar.set()

    elif card_num == 'not num' or len(message.text) != 16:
        await message.answer("HUMO kartangiz ustidagi 16 talik raqamni kiriting!")


# @dp.message_handler(state = EditWallet.EditHumoDate)
# async def change(message: types.Message, state:FSMContext):
#     if len(message.text) == 5:
#         addWallet_db(message, 'J')
#         await dp.bot.delete_message(chat_id = message.from_user.id, message_id=message.message_id-1)
#         await message.answer("Karta muvaffaqqiyatli qo'shildi✅", reply_markup = addWallet)
#         await Map.hamyonlar.set()

#     elif len(message.text) == 4:
#         uzcard_date = message.text[:2] + '/' + message.text[2:]
#         addWallet_db(message, 'J')
#         await message.answer("Karta muvaffaqqiyatli qo'shildi✅", reply_markup=addWallet)
#         await Map.hamyonlar.set()

#     else:
#         await message.answer("Noto'gri format kiritdingiz!\n\nFormat: 01/23 yoki 0123 kabi kiriting")

# Add QIWI
@dp.message_handler(state=EditWallet.EditQiwi)
async def change(message: types.Message, state: FSMContext):
    try:
        qiwi_num = int(message.text)
    except:
        qiwi_num = 'not num'
    print(len(message.text))
    if type(qiwi_num) == int and len(message.text) >= 8:
        addWallet_db(message, 'K')
        await message.answer("Binance PayID muvaffaqqiyatli qo'shildi✅", reply_markup=addWallet)
        await Map.hamyonlar.set()

    elif qiwi_num == 'not num' or len(message.text) != 9:
        await message.answer('Binance PayID ni kiriting.\n\nFormat: 426968609')


@dp.callback_query_handler(state=Map.hamyonlar, text='clear_wallets')
async def walletClear(call: types.CallbackQuery):
    clearWallets(call)
    await call.message.edit_text("Malumotlar o'chirildi✅")
