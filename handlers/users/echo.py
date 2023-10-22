from aiogram import types

from loader import dp

xabarlar = ["Signallarni ko'rish 📡", "Long 💰", "Short 💵"]
# Echo bot


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.text in xabarlar:
        await message.answer("🧑🏻‍💻 Developing...")
    else:
        await message.answer(message.text)
