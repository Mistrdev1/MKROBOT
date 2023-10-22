from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db


channels_copy_trade = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📈 Kunlik TOP", url="https://t.me/+eiHYhvPKDfBjN2Ji")
        ],
        [
            InlineKeyboardButton(text="📉 Haftalik TOP", url="https://t.me/+vpBQZUh0qwQ2MWYy")
        ],
        [
            InlineKeyboardButton(text="📆 Oylik TOP", url="https://t.me/+5aU4D7XHKzAxZDYy")
        ],
        [
            InlineKeyboardButton(text="📊 TOP Treyderlar", url="https://t.me/+yxAErHBeTjxiZTAy")
        ]
    ]
)


def notification_config_buttons(user_id):
    datas = db.get_notification_status(
        user_id=user_id,
        subscription="True",
    )
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    if datas[0] == "True":
        markup.insert(
            button=InlineKeyboardButton(
                text="🔴 Bildirishnomani o'chirish",
                callback_data="notification_off"
            )
        )
    if datas[0] == "False":
        markup.insert(
            button=InlineKeyboardButton(
                text="🟢 Bildirishnomani yoqish",
                callback_data="notification_on"
            )
        )
    if datas[0] == None:
        markup.insert(
            button=InlineKeyboardButton(
                text="🟢 Bildirishnomani yoqish",
                callback_data="notification_on"
            )
        )
    return markup



markup = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text="Tanlash 👤", callback_data="choose_trader"),
                InlineKeyboardButton(text="Takrorlash 🔄", url="https://www.binance.com/en/futures/")
            ]
        ]
    )
