from aiogram import types
from loader import dp, bot, db
from keyboards.inline.obmen import *
from keyboards.default.obmen_menu import *
from aiogram.dispatcher import FSMContext
from states.mapMenu import Map
from utils.db_api.dbxl import getWalletData
from keyboards.inline.choosevaluta import chooseValuta, clearWallets
from keyboards.default.wallet_keyboard import addWallet


@dp.message_handler(text="🔄 Obmen qilish")
async def abmen_handler(message: types.Message):
    await message.answer("<i>Tanlang:</i> 👇", reply_markup=mainMenu)


@dp.message_handler(text=['♻️ Valyuta ayirboshlash', '🗂Hamyonlar', '📈Kurs | Zahira', '🔁Almashinuvlar', 'ℹ️Ma\'lumotlar', '🍋QIWI identifikatsiya', '👥Referallar', '👨🏻‍💻Aloqa'], state="*")
async def change(message: types.Message, state: FSMContext):
    await state.finish()

    if message.text == '♻️ Valyuta ayirboshlash':
        await message.answer('⬆️Berish va ⬇️Olish valyutalarini tanlang', reply_markup=chooseValuta)

    elif message.text == '🗂Hamyonlar':
        await message.answer('🗂Hisoblar:', reply_markup=addWallet)

        uzcardNum = getWalletData(message.chat.id, 'uzcard')
        humoNum = getWalletData(message.chat.id, 'humo')
        ustdNum = getWalletData(message.chat.id, 'usdt')

        wallets = f"<b>📌UZCARD</b>:\n{uzcardNum}\n<b>📌HUMO:</b>\n{humoNum}\n<b>📌USDT:</b>\n{ustdNum}"
        await message.answer(wallets, reply_markup=clearWallets)
        await Map.hamyonlar.set()

    elif message.text == '📈Kurs | Zahira':
        datas = db.get_zahira(id=1)
        malumotlar = db.get_kurs(id=1)
        text = f"""
📉 Sotish kursi 
1 USDT = {malumotlar[2]} UZS

📉 Olish kursi 
1 USDT = {malumotlar[1]} UZS

💰Zahiralar

💵USDT = {datas[1]}
💳 SO'M = {datas[2]}
        """
        # text = "📉 Sotish kursi \n1 USDT = 180 UZS\n\n"
        # text += "📉 Olish kursi \n1 USDT = 180 UZS\n\n"
        # text += "=-=-=-=-=-=-=-=-=-=\n\n"
        # text += f"📈 USDT zahirasi\n USDT = {datas[1]}\n\n"
        # text += f"📈 SO'M zahirasi\n SO'M = {datas[2]}"
        await message.answer(text)
