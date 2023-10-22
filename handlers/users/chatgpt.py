from loader import dp, bot, db
from aiogram import types
from states.states import *
from keyboards.default.buttons import *
from aiogram.dispatcher import FSMContext
import openai


@dp.message_handler(text="🤖 Chatgpt bo'limi")
async def chatgpt_part(message: types.Message):
    datas = db.get_user_subs(message.from_user.id)
    if datas[0] == "True":
        await message.reply("📝<i>Savolingizni kiriting: </i>", reply_markup=types.ForceReply())
        await ChatgptState.question.set()
    if datas[0] == "False":
        await message.reply("❌ Siz ushbu tugmadan foydalana olmaysiz. Foydalanish uchun obunani sotib olishingiz kerak.")
    if datas[0] == "Waiting":
        await message.reply("❌ Siz ushbu tugmadan foydalana olmaysiz. Foydalanish uchun obunani sotib olishingiz kerak.")


@dp.message_handler(state=ChatgptState.question)
async def return_response(message: types.Message, state: FSMContext):
    text = message.text
    message_to_delete = (await message.answer("⏳ <b>Iltimos kuting...</b>")).message_id
    await state.finish()
    try:
        
        openai.api_key = "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"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.7
        )

        response = completion.choices[0].message['content']
        await message.reply(response, reply_markup=second_menu)
        await bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete)
    except:
        await message.reply("You exceeded your current quota, please check your plan and billing details.")
        await bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete)