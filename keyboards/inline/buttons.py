from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

panel = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⭕️ Obunani o'chirish",
                                 callback_data="obunani_ochirish")
        ],
        [
            InlineKeyboardButton(text="📤 Xabar yuborish",
                                 callback_data="send_post"),
            InlineKeyboardButton(text="🗃 Bazani yuklash",
                                 callback_data="base_download")
        ],
        [
            InlineKeyboardButton(
                text="💸 Obuna sotib olganlarga", callback_data="send_admins"),
            InlineKeyboardButton(text="📊 Statistika",
                                 callback_data="statistics")
        ],
        [
            InlineKeyboardButton(text="📝 Kurslarni kiritish",
                                 callback_data="kurslarni_tahrirlash"),
            InlineKeyboardButton(text="🖋 Zahiralarni kiritish",
                                 callback_data="zahiralarni_tahrirlash")
        ],
        [
            InlineKeyboardButton(text="❌ Panelni yopish",
                                 callback_data="close_panel")
        ]
    ]
)
base_types = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Excel", callback_data="type_excel"),
            InlineKeyboardButton(text="🗄 Sqlite", callback_data="type_sqlite")
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga", callback_data="back_to_panel"),
            InlineKeyboardButton(text="❌ Panelni yop",
                                 callback_data="close_panel")
        ]
    ]
)
cancel_button = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Bekor qilish",
                                 callback_data="cancel_action")
        ]
    ]
)


def del_channel():
    list = db.select_channels()
    markup = InlineKeyboardMarkup(row_width=2)
    for k in list:
        markup.insert(InlineKeyboardButton(
            text=f"{k[2]}", callback_data=f"delete_channel:{k[0]}"))
    markup.insert(InlineKeyboardButton(
        text="🔙 Orqaga", callback_data="back_to_panel"))
    markup.insert(InlineKeyboardButton(
        text="❌ Panelni yop", callback_data="close_panel"))
    return markup


def del_admin():
    admins = db.select_all_admins(status="Admin")
    markup = InlineKeyboardMarkup(row_width=2)
    for k in admins:
        markup.insert(InlineKeyboardButton(
            text=f"🧑‍💻 {k[3]}", callback_data=f"delete_admin:{k[1]}"))
    markup.insert(InlineKeyboardButton(
        text="🔙 Orqaga", callback_data="back_to_panel"))
    markup.insert(InlineKeyboardButton(
        text="❌ Panelni yop", callback_data="close_panel"))
    return markup


def change_admin_rights_1():
    admins = db.select_all_admins(status="Admin")
    markup = InlineKeyboardMarkup(row_width=2)
    for k in admins:
        markup.insert(InlineKeyboardButton(
            text=f"🧑‍💻 {k[3]}", callback_data=f"admin_rights:{k[1]}"))
    markup.insert(InlineKeyboardButton(
        text="🔙 Orqaga", callback_data="back_to_panel"))
    markup.insert(InlineKeyboardButton(
        text="❌ Panelni yop", callback_data="close_panel"))
    return markup


def change_admin_rights_2(admin_id):
    rights = db.get_admin_rights(admin_id=admin_id)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🧑‍💻 Adminlar: {rights[2]} ⚙️", callback_data=f"admin_change_admins:{admin_id}"),
                InlineKeyboardButton(
                    text=f"🔗 Kanallar: {rights[3]} ⚙️", callback_data=f"change_adminchanells:{admin_id}")
            ],
            [
                InlineKeyboardButton(
                    text=f"📤 Reklama: {rights[4]} ⚙️", callback_data=f"admin_change_ad:{admin_id}"),
                InlineKeyboardButton(
                    text=f"📤 Adminlarga post: {rights[5]} ⚙️", callback_data=f"admin_change_sendpost:{admin_id}")
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga", callback_data="back_to_panel"),
                InlineKeyboardButton(text="❌ Panelni yop",
                                     callback_data="close_panel")
            ]
        ]
    )
    return markup


def payment_buttons():
    payment_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔵 UzCard", callback_data=f"pay:UzCard"),
                InlineKeyboardButton(text="🟢 Humo", callback_data=f"pay:Humo")
            ],
            [
                InlineKeyboardButton(text="🟡 Visa", callback_data=f"pay:Visa"),
                InlineKeyboardButton(text="🟣 USDT TRC 20 ",
                                     callback_data=f"pay:usdtrc20")
            ]
        ]
    )
    return payment_buttons


def date_subscription(payment_method):
    date_subscription = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗓 Bir oy", callback_data=f"subscription_date:1:{payment_method}")
            ],
            [
                InlineKeyboardButton(
                    text="🗓 Ikki oy", callback_data=f"subscription_date:2:{payment_method}"),
                InlineKeyboardButton(
                    text="🗓 Doimiy", callback_data=f"subscription_date:3:{payment_method}")
            ]
        ]
    )
    return date_subscription


send_admin_screenshot = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📤 Adminga screenshot yuborish", callback_data="send_admin_screenshot")
        ]
    ]
)


def admin_check_buttons(user_id):
    check_admin_user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash ✅",
                                     callback_data=f"checked:{user_id}"),
                InlineKeyboardButton(text="Rad etish ❌",
                                     callback_data=f"rejected:{user_id}")
            ]
        ]
    )
    return check_admin_user


check_datas_user = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha ✅", callback_data="yes_right"),
            InlineKeyboardButton(text="Yo'q ❌", callback_data="no_wrong")
        ]
    ]
)


def share_btn(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Do'stlarga yuborish 📲", switch_inline_query=f"{user_id}")
            ]
        ]
    )
    return markup


def answer_question(user_id):
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="↪️ Javob berish",
                                     callback_data=f"answerquestion:{user_id}")
            ]
        ]
    )
    return markup


def start_bot(user_id):
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Botga kirish", url=f"https://t.me/MKSIGNAL_RoBot?start={user_id}")
            ]
        ]
    )
    return markup


Javob = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data='A'),
            InlineKeyboardButton(text="B", callback_data='B'),
            InlineKeyboardButton(text="C", callback_data='C')
        ]
    ]
)


p2p_menyu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Spredni o'zgartirish",
                callback_data="change_spread"
            )
        ],
        [
            InlineKeyboardButton(
                text="Birjalarni tanlash",
                callback_data="choose_birjas"
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️",
                callback_data="about_birja"
            ),
            InlineKeyboardButton(
                text="🏠",
                callback_data="cancel_birjas"
            )
        ]
    ]
)


def change_spred_btn(id_user):
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Spred 0.3%",
                    callback_data="change_spred:03"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Spred 0.5%",
                    callback_data="change_spred:05"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Spred 1.5%",
                    callback_data="change_spred:15"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Spred 3%",
                    callback_data="change_spred:30"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Spred 5%",
                    callback_data="change_spred:50"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="bekorqilishtugmasiuchun"
                ),
            ]
        ]
    )
    return markup

# Binance 
# Huobi Global
# Bybit
# OKX
def choosebirjas(id_user):
    malumotlar = db.select_user_valyuta(id_user)
    if malumotlar[2] == "True":
        text_binance = "✅ Binance"
        callback_data_binance = "choose_birja:binance:False"
    else:
        text_binance = "Binance"
        callback_data_binance = "choose_birja:binance:True"
    if malumotlar[3] == "True":
        text_houbi = "✅ Huobi Global"
        callback_data_huobi = "choose_birja:huobiglobal:False"
    else:
        text_houbi = "Huobi Global"
        callback_data_huobi = "choose_birja:huobiglobal:True"
    if malumotlar[4] == "True":
        text_bybit = "✅ Bybit"
        callback_data_bybit = "choose_birja:bybit:False"
    else:
        text_bybit = "Bybit"
        callback_data_bybit = "choose_birja:bybit:True"
    if malumotlar[5] == "True":
        text_okx = "✅ OKX"
        callback_data_okx = "choose_birja:okx:False"
    else:
        text_okx = "OKX"
        callback_data_okx = "choose_birja:okx:True"
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text_binance, callback_data=callback_data_binance)
            ],
            [
                InlineKeyboardButton(text=text_houbi, callback_data=callback_data_huobi)
            ],
            [
                InlineKeyboardButton(text=text_bybit, callback_data=callback_data_bybit)
            ],
            [
                InlineKeyboardButton(text=text_okx, callback_data=callback_data_okx)
            ],
            [
                InlineKeyboardButton(text="⬅️", callback_data="bekorqilishtugmasiuchun"),
                InlineKeyboardButton(text="🏠", callback_data="cancel_birjas")
            ]
        ]
    )
    return markup