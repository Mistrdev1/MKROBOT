from aiogram import types
from data.config import DEVELOPER
from loader import db, dp, bot
from aiogram.types import Message
from filters.channel import Kanal
from aiogram.utils import exceptions
from utils.utilities import text_editor
from keyboards.inline.copy_trade import markup
import asyncio

# COPY_TRADE_KANAL_ID = -1001746850628
Long_SHORT_channel = -1002022338980
SIGNAL_KANAL_ID = -1001825501226
# SIGNAL_KANAL_ID = -1001653133310
BIRJA_KANAL_ID = -1001942837259
COPY_TRADE_CHANNELS = [-1001898739360, -1001845660743, -1001817112761, -1001700976599, -1001696486614]


@dp.channel_post_handler(Kanal(), content_types=types.ContentTypes.ANY)
async def send_short_messages_to_users(message: Message):
    datas = db.select_users_subscription(subscription="True")
    ##############
    ## COPY TRADE KANAL UCHUN YOZILGAN
    if message.chat.id == Long_SHORT_channel:
        print("Long/Short uchun IF ishlayapti...")
        try:
            for data in datas:
                # print(datas[12])
                try:
                    if data[12] == "True":
                        # print(data[12], data[1])
                        # print(message.chat.id)
                        # print(message.message_id)
                        await bot.copy_message(
                            chat_id=data[1],
                            from_chat_id=message.chat.id,
                            message_id=message.message_id
                        )
                        # print(data[2], data[12])
                        await asyncio.sleep(0.4)
                    else:
                        pass
                except exceptions.BotBlocked:
                    await bot.send_message(
                        chat_id=DEVELOPER,
                        text=f"Bot bloklangan!"
                    )
                    try:
                        db.delete_user(
                            user_id=data[1]
                        )
                        await bot.send_message(
                            chat_id=DEVELOPER,
                            text=f"Botni bloklagan foydalanuvchi o'chirib tashlandi!"
                        )
                    except Exception as err:
                        await bot.send_message(
                            chat_id=DEVELOPER,
                            text=f"Botni bloklagan foydalanuvchi o'chirib tashlashda xatolik ketdi: {err}"
                        )
                except exceptions.ChatNotFound:
                    print("Chat topilmadi")
                    # await bot.send_message(
                    #     chat_id=DEVELOPER,
                    #     text=f"Chat topilmadi!"
                    # )
                    pass
                except exceptions.UserDeactivated:
                    # await bot.send_message(
                    #     chat_id=DEVELOPER,
                    #     text=f"Foydalanuvchi hisobi o'chirib tashlangan! ✅ ✅ ✅"
                    # )
                    pass
                except exceptions.MessageIdInvalid:
                    # await bot.send_message(
                    #     chat_id=DEVELOPER,
                    #     text="Yuborish uchun xabar topilmadi."
                    # )
                    pass
                except Exception as err:
                    pass
        except Exception as err:
            await bot.send_message(
                chat_id=DEVELOPER,
                text=f"Botdagi azolarga Long/Short ni jo'natishda xatolik ketayapti: {err}"
            )

    ##############
    # SIGNAL KANAL UCHUN YOZILGAN
    if message.chat.id == SIGNAL_KANAL_ID:
        print("Signal uchun IF ishlayapti...")
        for data in datas:
            try:
                xabar_id = message.message_id
                await bot.copy_message(
                    chat_id=data[1],
                    from_chat_id=message.chat.id,
                    message_id=xabar_id
                )
                await asyncio.sleep(0.8)
            except exceptions.BotBlocked:
                await bot.send_message(
                    chat_id=DEVELOPER,
                    text=f"Bot bloklangan!"
                )
                try:
                    db.delete_user(
                        user_id=data[1]
                    )
                    await bot.send_message(
                        chat_id=DEVELOPER,
                        text=f"Botni bloklagan foydalanuvchi o'chirib tashlandi!"
                    )
                except Exception as err:
                    await bot.send_message(
                        chat_id=DEVELOPER,
                        text=f"Botni bloklagan foydalanuvchi o'chirib tashlashda xatolik ketdi: {err}"
                    )
            except exceptions.ChatNotFound:
                await bot.send_message(
                    chat_id=DEVELOPER,
                    text=f"Chat topilmadi!"
                )
            except exceptions.UserDeactivated:
                try:
                    db.delete_user(
                        user_id=data[1]
                    )
                    await bot.send_message(
                        chat_id=DEVELOPER,
                        text="O'chirilgan hisob bazadan muvaffaqiyatli o'chirib tashlandi ✅"
                    )
                except Exception as err:
                    await bot.send_message(
                        chat_id=DEVELOPER,
                        text=f"❌ O'chirilgan hisobli foydalanuvchini o'chirishda xatolik ketdi! {err}"
                    )
            except exceptions.MessageIdInvalid:
                await bot.send_message(
                    chat_id=DEVELOPER,
                    text="Yuborish uchun xabar topilmadi."
                )
            except Exception as err:
                await bot.send_message(
                    chat_id=DEVELOPER,
                    text=f"Bot SIGNALLARNI copy qilishda qiynalyapti: {err}"
                )












    ##############
    # BIRJALAR KANAL UCHUN YOZILGAN
    elif message.chat.id == BIRJA_KANAL_ID:
        print("Birja uchun IF ishlayapti...")
        for data in datas:
            malumotlar = message.text.rsplit(" ")
            sozlar = db.select_user_valyuta(data[1])
            if sozlar is not None:
                birjalar = []
                if sozlar[2] == "True":
                    target1 = "#Binance"
                    birjalar.append("#Binance")
                else:
                    target1 = "sdfhsfgh48648fg"
                if sozlar[3] == "True":
                    target2 = "#HuobiGlobal"
                    birjalar.append("#HuobiGlobal")
                else:
                    target2 = "aawsfdlhiouwnfv"
                if sozlar[4] == "True":
                    target3 = "#Bybit"
                    birjalar.append("#Bybit")
                else:
                    target3 = "adfasfasdasdv"
                if sozlar[5] == "True":
                    target4 = "#OKX"
                    birjalar.append("#OKX")
                else:
                    target4 = "asgdazxcvzvc"
                for r in birjalar:
                    if r in malumotlar[0]:
                        print("Ishlayapti...")
                        try:
                            son = float(malumotlar[2].replace(
                                "%\n", ":").rsplit(":")[0].replace("+", ""))
                        except:
                            print("Yana xatolik chiqayapti!")
                        try:
                            if data[-2] == None:
                                await bot.send_message(
                                    chat_id=data[1],
                                    text=text_editor(message.text)
                                )
                            else:
                                foiz = float(data[-2])
                                if foiz > son:
                                    pass
                                else:
                                    await bot.send_message(
                                        chat_id=data[1],
                                        text=text_editor(message.text)
                                    )
                                    await asyncio.sleep(1)
                        except exceptions.BotBlocked:
                            await bot.send_message(
                                chat_id=DEVELOPER,
                                text=f"Bot bloklangan!"
                            )
                            try:
                                db.delete_user(
                                    user_id=data[1]
                                )
                                await bot.send_message(
                                    chat_id=DEVELOPER,
                                    text=f"Botni bloklagan foydalanuvchi o'chirib tashlandi!"
                                )
                            except Exception as err:
                                await bot.send_message(
                                    chat_id=DEVELOPER,
                                    text=f"Botni bloklagan foydalanuvchi o'chirib tashlashda xatolik ketdi: {err}"
                                )
                        except exceptions.ChatNotFound:
                            pass
                            # await bot.send_message(
                            #     chat_id=DEVELOPER,
                            #     text=f"Chat topilmadi!"
                            # )
                        except exceptions.UserDeactivated:
                            try:
                                db.delete_user(
                                    user_id=data[1]
                                )
                                await bot.send_message(
                                    chat_id=DEVELOPER,
                                    text="O'chirilgan hisob bazadan muvaffaqiyatli o'chirib tashlandi ✅"
                                )
                            except Exception as err:
                                await bot.send_message(
                                    chat_id=DEVELOPER,
                                    text=f"❌ O'chirilgan hisobli foydalanuvchini o'chirishda xatolik ketdi! {err}"
                                )
                        except exceptions.MessageIdInvalid:
                            await bot.send_message(
                                chat_id=DEVELOPER,
                                text="Yuborish uchun xabar topilmadi."
                            )
                        except Exception as err:
                            await bot.send_message(
                                chat_id=DEVELOPER,
                                text=f"Bot BIRJALARNI copy qilishda qiynalyapti: {err}"
                            )
                birjalar.clear()
            else:
                pass







    elif message.chat.id in COPY_TRADE_CHANNELS:
        try:
            text = message.text.split(" ")
            users = db.select_trader(
                name=text[0]
            )
            if users:
                for user in users:
                    await bot.send_message(
                        chat_id=user[1],
                        text=message.text
                    )
            else:
                pass

        except:
            pass
        await message.edit_reply_markup(reply_markup=markup)





    else:
        pass
