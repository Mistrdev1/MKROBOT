from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='♻️ Valyuta ayirboshlash')
        ],
        [
            KeyboardButton(text='🗂Hamyonlar'),
            KeyboardButton(text='📈Kurs | Zahira')
        ],
        [
            KeyboardButton(text='🔙Asosiy menyu')
        ],
    ], one_time_keyboard=True)
