from typing import Union
from aiogram import Bot
from data.config import CHANNELS
from loader import db, dp, bot



async def check(user_id, channel: Union[int, str]):
    bot = Bot.get_current()
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.is_chat_member()


async def check_status(user_id):
    final_status = True
    if CHANNELS:
        for channel in CHANNELS:
            status = await check(user_id=user_id, channel=channel)
            final_status *= status
    return final_status