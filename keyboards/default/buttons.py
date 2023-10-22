from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton("👤 Biz haqimizda")
        ],
        [
            KeyboardButton("📎 Referal bo'limi"),
            KeyboardButton("💴 Referal balans")
            
        ],
        [
            KeyboardButton("📶 Signal sotib olish"),
            KeyboardButton("📊 Natijalar")
        ],
        [
            KeyboardButton("🔄 Obmen qilish"),
            KeyboardButton("🧑🏻‍💻 Operator bilan bog'lanish"),
        ],
        [
            KeyboardButton("📝 Test ishlash")
        ]
    ]
)


second_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("👤 Biz haqimizda")
        ],
        [
            KeyboardButton("📎 Referal bo'limi"),
            KeyboardButton("💴 Referal balans"),
        ],
        [
            KeyboardButton("📶 Signal sotib olish"),
            KeyboardButton("📊 Natijalar")
        ],
        [
            KeyboardButton("🧑🏻‍💻 Operator bilan bog'lanish"),
            KeyboardButton("🤖 Chatgpt bo'limi"),
        ],
        [
            KeyboardButton("💎 Copy Trade"),
            KeyboardButton("⏰ Obuna muddati")
        ],
        [
            KeyboardButton("🔄 Obmen qilish"),
            KeyboardButton("📌 Qanday savdo qilish kerak?"),
        ],
        [
            KeyboardButton("♻️ P2P Arbitraj"),
            KeyboardButton("📊 Long/Short"),
        ]
    ]
)

contact_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton("☎️ Telefon raqamni yuborish", request_contact=True)
        ]
    ]
)

third_part = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("📶 Signal haqida ma'lumot"),
            KeyboardButton("♻️ Obunani sotib olish")
        ],
        [
            KeyboardButton("🏠 Bosh menyu")
        ]
    ]
)

back_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("🔙 Bekor qilish")
        ]
    ]
)


results_part = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("📊 Natijalarni ko'rish"),
            KeyboardButton("📤 Natijalarni yuborish")
        ],
        [
            KeyboardButton("🏠 Bosh menyu")
        ]
    ]
)



copy_trade_buttons = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("ℹ️ Copy Trade haqida"),
            KeyboardButton("💎 Copy Trade kanallar")
        ],
        [
            KeyboardButton("🏠 Bosh menyu")
        ]
    ]
)


leave_test_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("🔙 Testdan chiqish")
        ]
    ]
)



