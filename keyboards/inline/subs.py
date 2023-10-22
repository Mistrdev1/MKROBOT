from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import CHANNELS
from utils.misc import subscription
from loader import bot, db

async def SubscChanBtn(user_id):
    btn = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        status = await subscription.check(user_id=user_id, channel=channel)
        chan_info = await bot.get_chat(channel)
        if not status:
            btn.insert(InlineKeyboardButton(text=chan_info.title, url=await chan_info.get_url()))
    btn.insert(InlineKeyboardButton(text='✅ A’zo bo’ldim', callback_data='check_subsciption'))
    return btn