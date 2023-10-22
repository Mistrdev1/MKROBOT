from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


obmen_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Almashtirish",
                callback_data="almashtirish"
            ),
            InlineKeyboardButton(
                text="💳 Hamyonlar",
                callback_data="hamyonlar"
            )
        ],
        [
            InlineKeyboardButton(
                text="💰 Kurs Zahira",
                callback_data="kurszahira"
            )
        ]
    ]
)


almashtirish_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📤 Berish",
                callback_data="berish"
            ),
            InlineKeyboardButton(
                text="📥 Olish",
                callback_data="olish"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_obmen"
            )
        ]
    ]
)


def givOrTake(berish, olish):
    choose_type = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = f"🔹 Berishni kiritish * {berish}", callback_data = "choosen_berish")
            ],
            [
                InlineKeyboardButton(text = f"♦️ Olishni kiritish * {olish}", callback_data = "choosen_olish")
            ],
            [
                InlineKeyboardButton(text = f"🚫 Bekor qilish", callback_data='cancel')
            ]
        ]
        )
    return choose_type


kurs_zahirasi = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Kurs zahirasini ko'rish",
                callback_data="show_course_backup"
            )
        ]
    ]
)