from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def success_or_fail(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Muvaffaqiyatli",
                                     callback_data=f'trans_success:{user_id}')
            ],
            [
                InlineKeyboardButton(text="❌Bekor qilish",
                                     callback_data=f'trans_fail:{user_id}'),
            ],
        ])
    return markup
