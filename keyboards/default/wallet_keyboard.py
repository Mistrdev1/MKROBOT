from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

addWallet = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='➕UZCARD'),
            KeyboardButton(text='➕HUMO'),
            KeyboardButton(text='➕USDT')
        ],
        [
            KeyboardButton(text='🔙Asosiy menyu')
        ]
    ], resize_keyboard=True, one_time_keyboard=True)
