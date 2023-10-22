from aiogram import types
from loader import db, dp, bot
from keyboards.inline.buttons import start_bot
import uuid


@dp.inline_handler()
async def emty_query(query: types.InlineQuery):
    user_suu = await bot.get_me()
    responses = []
    try:
        if query.query == "":
            caption = f"<i>🔗 Quyidagi havola orqali botga kiring va siz ham soqqa qilishni boshlang. 💸 👇</i>\n\n"
            caption += f"👇 Boshlash uchun bosing:\nhttps://t.me/{user_suu.username}"
            responses.append(
                types.InlineQueryResultArticle(
                    id=f"{uuid.uuid4()}",
                    title=f"<b>{user_suu.full_name}</b> - Soqqalar makoni",
                    input_message_content=types.InputTextMessageContent(
                        message_text=caption,
                        parse_mode="HTML"
                    ),
                    url="https://t.me/+sVn66CXL5Eg0YmY6",
                    description="Botga kiring va soqqa tagida qoling",
                    thumb_url="https://static5.tgstat.ru/channels/_0/b9/b9c06851420445fe503b50c70a125efb.jpg"
                ),
            )
            await query.answer(responses, cache_time=1)
        else:
            if db.check_user(user_id=query.query):
                print("The bot is working...")
                malumotlar = db.select_user_datas(user_id=query.query)
                caption = f"✅ <b>«{user_suu.full_name}»</b> - soqqalar makoni\n\n"
                caption += f"🎈 <a href='tg://user?id={malumotlar[1]}'><b>{malumotlar[3]}</b></a> do'stingizdan unikal havola-taklifnoma.\n"
                caption += f"<i>🔗 Quyidagi havola orqali botga kiring va siz ham soqqa qilishni boshlang. 💸 👇</i>\n\n"
                caption += f"👇 Boshlash uchun bosing:\nhttps://t.me/{user_suu.username}?start={malumotlar[1]}"
                responses.append(
                    types.InlineQueryResultCachedPhoto(
                        id=f"{malumotlar[0]}",
                        # photo_file_id="AgACAgIAAxkBAAJnN2RmEmzF3NE9pi4kcQX4hBOshqmZAAL2yDEbeuoxS6nlHxmFYoISAQADAgADeAADLwQ",
                        photo_file_id="AgACAgIAAxkBAAIDjmRZsZ8Nij37N6xOpDU0yFDxckQoAAJ8wzEbBtTQSleVw2_r3hpaAQADAgADeAADLwQ",
                        title=f"{malumotlar[3]} - Unikal taklif noma",
                        description="Test uchun description",
                        caption=caption,
                        reply_markup=start_bot(user_id=malumotlar[1])
                    )
                )
                await query.answer(results=responses, cache_time=1)
            else:
                caption = f"<i>🔗 Quyidagi havola orqali botga kiring va siz ham soqqa qilishni boshlang. 💸 👇</i>\n\n"
                caption += f"👇 Boshlash uchun bosing:\nhttps://t.me/{user_suu.username}"
                responses.append(
                    types.InlineQueryResultArticle(
                        id=f"{uuid.uuid4()}",
                        title=f"<b>{user_suu.full_name}</b> - Soqqalar makoni",
                        input_message_content=types.InputTextMessageContent(
                            message_text=caption,
                            parse_mode="HTML"
                        ),
                        url="https://t.me/+sVn66CXL5Eg0YmY6",
                        description="Botga kiring va soqqa tagida qoling",
                        thumb_url="https://static5.tgstat.ru/channels/_0/b9/b9c06851420445fe503b50c70a125efb.jpg"
                    ),
                )
                await query.answer(responses, cache_time=1)
    except Exception as err:
        await bot.send_message(chat_id=query.from_user.id, text=f"Xatolik ketdi: {err}")
