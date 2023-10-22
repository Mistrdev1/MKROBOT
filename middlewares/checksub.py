import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.subs import *
from utils.misc import subscription
from loader import bot, db
from data.config import CHANNELS


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):        
        if update.message:
            user = update.message.from_user.id
            if update.message.get_command() == CommandStart():
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        final_status = True
        if CHANNELS:
            for channel in CHANNELS:
                status = await subscription.check(user_id=user, channel=channel)
                final_status *= status
            if not final_status:
                await update.message.answer(
                    text="Tanlovda ishtirok etish uchun quyidagi kanalga a’zo bo’ling. Keyin “✅ A’zo bo’ldim” tugmasini bosing.", 
                                            reply_markup=await SubscChanBtn(user))
                raise CancelHandler()