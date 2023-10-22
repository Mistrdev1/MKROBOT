from loader import db, bot, dp
from aiogram import types
from keyboards.inline.buttons import *
from states.states import DefaultState
from states.zahiras import ZahiraTahrirlash, KursTahrirlash
from states.blockState import BlockUserState
from aiogram.dispatcher import FSMContext
from xlsxwriter.workbook import Workbook
import os
import sqlite3
from asyncio import sleep
import asyncio
from datetime import datetime
from data.config import DEVELOPER
from keyboards.default.buttons import main_menu

# /panel komandasi uchun admin panel ochadigan handler


@dp.message_handler(commands=['panel'])
async def admin_panel(message: types.Message):
    user_status = db.get_admins(user_id=message.from_user.id)[0]
    if user_status == "Admin":
        await message.answer("<i><b>🧑‍💻 Siz admin panelidasiz.</b></i>", reply_markup=panel)
        await message.delete()
    else:
        await message.answer("🧑‍💻 Siz admin emassiz. ❌")

# Admin panelni yopadigan handler


@dp.callback_query_handler(text="close_panel")
async def close_panel(call: types.CallbackQuery):
    await call.message.delete()

# Bazani yuklab olish uchun handler


@dp.callback_query_handler(text="base_download")
async def base_download(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        await call.message.edit_text(text="<i>Qay holatda bazani yuklab olmoqchisiz?</i>")
        await call.message.edit_reply_markup(reply_markup=base_types)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")

# orqaga qaytaruvchi handler


@dp.callback_query_handler(text="back_to_panel")
async def back(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        await call.message.edit_text(text="<i><b>Siz admin panelidasiz. 🧑‍💻</b></i>")
        await call.message.edit_reply_markup(reply_markup=panel)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="add_channel")
async def add_channel(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[3] == "Yes":
            await DefaultState.text.set()
            await call.message.edit_text(text="<i><b>📛 Kanal usernamesini yoki ID sini kiriting: </b></i>")
            await call.message.edit_reply_markup(reply_markup=cancel_button)
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.message_handler(state=DefaultState.text)
async def add_channel(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit() or matn.startswith("@"):
        try:
            if db.check_channel(channel_id=message.text):
                await message.answer("<i>❌Bu kanal qo'shilgan! Boshqa kanal qo'shing!</i>", reply_markup=cancel_button)
            else:
                try:
                    deeellll = await bot.send_message(chat_id=message.text, text=".")
                    await bot.delete_message(chat_id=message.text, message_id=deeellll.message_id)
                    db.add_channel(
                        name="",
                        channel_id=message.text
                    )
                    await message.answer("<i><b>Channel succesfully added ✅</b></i>")
                    await message.answer("<i>Siz admin panelidasiz. 🧑‍💻</i>", reply_markup=panel)
                    await state.finish()
                except:
                    await message.reply("""<i><b>
Bu kanalda admin emasman!⚙️
Yoki siz kiritgan username ga ega kanal mavjud emas! ❌
Kanalga admin qilib qaytadan urinib ko'ring yoki to'g'ri username kiriting.🔁
                    </b></i>""", reply_markup=cancel_button)
        except Exception as err:
            await message.answer(f"Xatolik ketdi: {err}")
            await state.finish()
    else:
        await message.answer("Xato kiritdingiz.", reply_markup=cancel_button)


@dp.callback_query_handler(text="cancel_action", state="*")
async def cancel_try(call: types.CallbackQuery, state: FSMContext):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        await call.message.edit_text(text="<i><b>Siz admin panelidasiz. 🧑‍💻</b></i>")
        await call.message.edit_reply_markup(reply_markup=panel)
        await call.answer("Bekor qilindi!")
        await state.finish()
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="delete_channel")
async def del_cahnnce(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[3] == "Yes":
            await call.message.edit_text("<i><b>💻 Qaysi kanalni o'chirmoqchisiz tanlang.</b></i>")
            await call.message.edit_reply_markup(reply_markup=del_channel())
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text_contains="delete_channel:")
async def deletee_channlerr(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[3] == "Yes":
            id = call.data.replace("delete_channel:", "")
            try:
                db.delete_channel(
                    id=id
                )
                await call.answer("Channel deleted successfully ✅")
                await call.message.edit_text("<i><b>Siz admin panelidasiz.</b></i>")
                await call.message.edit_reply_markup(reply_markup=del_channel())
            except Exception as err:
                await call.message.answer(err)
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)


@dp.callback_query_handler(text="channel_list")
async def channel_list(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[3] == "Yes":
            royxat = db.select_channels()
            text = "🔰 Kanallar ro'yxati:\n\n"
            son = 0
            for o in royxat:
                son += 1
                text += f"{son}. {o[2]}\n💠 Username: {o[2]}\n\n"
            await call.message.edit_text(text=text)
            await call.message.edit_reply_markup(reply_markup=cancel_button)
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="admins_list")
async def get_list_of_admins(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[2] == "Yes":
            adminlar = db.select_all_admins(status="Admin")
            text = "🧑‍💻 Adminlar ro'yxati:\n\n"
            son = 0
            for o in adminlar:
                son += 1
                text += f"{son}. <a href='tg://user?id={o[1]}'>{o[3]}</a> 🧑‍💻\n💠 Username: @{o[2]}\n\n"
            await call.message.edit_text(text=text)
            await call.message.edit_reply_markup(reply_markup=change_admin_rights_1())
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="add_admin")
async def add_admin(call: types.CallbackQuery):
    if call.from_user.id == 1849953640:
        await DefaultState.admin.set()
        await call.message.edit_text("<i><b>Admin qilmoqchi bo'lgan foydalanuvchining ID sini kiriting.\nSiz kiritgan id ga ega foydalanuvchi bazada bo'lishi kerak.</b></i>")
        await call.message.edit_reply_markup(reply_markup=cancel_button)
    else:
        await call.answer("☠ Siz ushbu buyruqdan foydalana olmaysiz. ❌", show_alert=True)


@dp.message_handler(state=DefaultState.admin)
async def add_admin(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit():
        if db.check_admin(admin_id=matn):
            await message.answer("<b><i>🧑‍💻 Siz kiritgan ID bo'yicha admin avvaldan mavjud.</i></b> ♻️", reply_markup=cancel_button)
        else:
            try:
                if db.check_user(user_id=matn):
                    try:
                        db.update_status(
                            status="Admin",
                            user_id=matn
                        )
                        await bot.send_message(chat_id=matn, text="""<i><b>
    Tabriklaymiz 🎉,
    Siz botimizda admin qilib tayinlandingiz.✅
    Marahamat /panel buyrugini yuboring tekshirib ko'rishingiz mumkin. 👩🏻‍💻
    ⚙️ Hozirda siz qila oladigan funksiyalar:
    - Kanal qo'shib o'chirish: No ❌
    - Admin qo'shish va o'chirish: No ❌
    - Reklama yuborish: No ❌
    - Adminlarga xabar yuborish: No ❌
    - Bazani yuklab olish: Yes ✅
    - Statistikani ko'rish: Yes ✅ 
    Bosh admin sizning huquqlaringizni boshqarishi mumkin. 💻</b></i>""")
                        db.add_admin(
                            admin_id=matn,
                            admins="No",
                            channels="No",
                            send_post="No",
                            admin_post="No",
                        )
                        await message.answer("<i><b>🧑‍💻Admin added successfully.✅</b></i>")
                        await message.answer("<i><b>🧑‍💻 Siz admin panelidasiz. </b></i>", reply_markup=panel)
                        await state.finish()
                    except Exception as err:
                        await message.answer(f"🤖 Log such add admin: {err}")
                        await state.finish()
                else:
                    await message.answer("<i>Siz kiritgan id bo'yicha foydalanuvchi topilmadi.❌\nIltimos qaytadan to'g'ri id kiriting.🔁</i>", reply_markup=cancel_button)
            except Exception as err:
                await message.answer(f"🤖Log such check_user in start: {err}")
                await state.finish()
    else:
        await message.answer("<i>Iltimos raqamlardan tashkil topgan id kiriting. 🔁</i>", reply_markup=cancel_button)


@dp.callback_query_handler(text="delete_admin")
async def delete_admin(call: types.CallbackQuery):
    if call.from_user.id == 1849953640:
        await call.message.edit_text(text="<i><b>🧑‍💻Qaysi adminni o'chirmoqchi bo'lsangiz o'shaning ustiga bossangiz o'chiriladi!</b></i>")
        await call.message.edit_reply_markup(reply_markup=del_admin())
    else:
        await call.answer("☠ Siz ushbu buyruqdan foydalana olmaysiz. ❌", show_alert=True)


@dp.callback_query_handler(text_contains="delete_admin:")
async def delete_admin(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        id_Admin = call.data.replace("delete_admin:", "")
        try:
            db.update_status(
                status="User",
                user_id=id_Admin
            )
            db.delete_admin(
                admin_id=id_Admin
            )
            await bot.send_message(chat_id=id_Admin, text="<i><b>🔰 Siz botimizdan adminlik huquqlaridan ayrildingiz. ❌</b></i>")
            await call.answer("<b><i>Admin removed successfully.</i></b>")
            await call.message.edit_text(text="<b><i>Siz admin panelidasiz</i></b>")
            await call.message.edit_reply_markup(reply_markup=panel)
        except Exception as err:
            await call.answer("Xatolik ketdi!")
            await call.message.answer(f"🤖 Log such update status: {err}")
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="type_sqlite")
async def get_Sqlite_base(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        base = types.InputFile(path_or_bytesio="data/main.db")
        bot_sue = await bot.get_me()
        await call.message.answer_document(document=base, caption=f"🤖 Malumotlar bazasi. \n🔥 @{bot_sue.username} - zo'r bot. ✅")
        await call.message.answer("💻 <b><i>Siz admin panelidasiz</i></b>", reply_markup=panel)
        await call.message.delete()
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="type_excel")
async def get_base(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        try:
            workbook = Workbook('data/Excel.xlsx')
            worksheet = workbook.add_worksheet()
            conn = sqlite3.connect('data/main.db')
            c = conn.cursor()
            c.execute(f"select * from Users")
            mysel = c.execute(f"select * from Users ")
            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    worksheet.write(i, j, row[j])
            workbook.close()
        except Exception as err:
            await call.answer(f"Bazagani excelga yozishda xatolik: \n\n{err}")
        file = types.InputFile(path_or_bytesio="data/Excel.xlsx")
        user = await bot.get_me()
        await call.message.answer_document(document=file, caption=f"<i><b>📂 Botdagi barcha userlar haqidagi ma'lumotlar mana shu excel faylda! ✅\n\n🔥 @{user.username} - zo'r bot. ✅</b></i>")
        await call.message.answer("💻 <b><i>Siz admin panelidasiz</i></b>", reply_markup=panel)
        await call.message.delete()
        os.remove(path="data/Excel.xlsx")
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.callback_query_handler(text="send_post")
async def send_posts(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[4] == "Yes":
            await call.message.edit_text("<b><i>Yubormoqchi bo'lgan postingizni kiriting. </i></b>")
            await call.message.edit_reply_markup(reply_markup=cancel_button)
            await DefaultState.post.set()
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)

    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.message_handler(state=DefaultState.post, content_types=types.ContentTypes.ANY)
async def send_all(message: types.Message, state: FSMContext):
    users = db.select_all_admins(status="User")
    await state.finish()
    try:
        send = 0
        cross = 0
        text = ""
        text0 = 0
        dell_messaga = await message.answer("⏳ Barcha foydalanuvchilarga yuborilmoqda...\n")
        for user in users:
            try:
                await bot.copy_message(chat_id=user[1],
                                       from_chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       caption=message.caption,
                                       reply_markup=message.reply_markup)
                send += 1
                await asyncio.sleep(0.8)
            except Exception as err:
                print(err)
                cross += 1
        await dell_messaga.delete()
        user = await bot.get_me()
        text += f"<b>Botdagi jami foydalanuvchilar: {db.count_users()[0]} taga teng.\nShundan:\n</b>"
        text += f"<i>\n✅ {send} ta foydalanuvchiga yuborildi.\n❌ {cross} ta foydalanuvchiga yuborilmadi!\n\n🤖@{user.username} - Zo'r bot 💎</i>"
        deletaion = await message.answer(text=text)
        await message.answer("<i><b>🧑‍💻 Siz admin panelidasiz. </b></i>", reply_markup=panel)
        await state.finish()
        await sleep(60)
        await bot.delete_message(chat_id=message.from_user.id, message_id=deletaion.message_id)
    except Exception as err:
        await message.answer(f"{err}")


@dp.callback_query_handler(text="send_admins")
async def send_admins(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        rights = db.get_admin_rights(admin_id=call.from_user.id)
        if rights[5] == "Yes":
            await call.message.edit_text("<b><i>Yubormoqchi bo'lgan postingizni kiriting. </i></b>")
            await call.message.edit_reply_markup(reply_markup=cancel_button)
            await DefaultState.adminss.set()
        else:
            await call.answer("🧑‍💻 Sizning bu tugmadan foydalanish uchun huquqingiz cheklangan. ❌", show_alert=True)
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")


@dp.message_handler(state=DefaultState.adminss, content_types=types.ContentTypes.ANY)
async def send_Admins(message: types.Message, state: FSMContext):
    users = db.select_users_subscription(subscription="True")
    try:
        send = 0
        cross = 0
        text = ""
        for user in users:
            try:
                await bot.copy_message(chat_id=user[1],
                                       from_chat_id=message.chat.id,
                                       message_id=message.message_id)
                # text += f"✅ Yuborildi!\n🆔 ID: {user[1]}\n🪪 Username: {user[2]}\n📝 FullName: {user[3]}\n\n"
                send += 1
            except Exception as err:
                cross += 1
        user = await bot.get_me()
        text += f"<b>Botdagi jami obuna sotib olganlar: {len(users)} taga teng.\nShundan:\n</b>"
        text += f"<i>\n✅ {send} ta foydalanuvchiga yuborildi.\n❌ {cross} ta foydalanuvchiga yuborilmadi!\n\n🤖@{user.username} - Zo'r bot 💎</i>"
        deletaion = await message.answer(text=text)
        await message.answer("<i><b>🧑‍💻 Siz admin panelidasiz. </b></i>", reply_markup=panel)
        await state.finish()
        await sleep(60)
        await bot.delete_message(chat_id=message.from_user.id, message_id=deletaion.message_id)
    except Exception as err:
        await message.answer(f"{err}")


@dp.callback_query_handler(text="statistics")
async def get_statistics(call: types.CallbackQuery):
    user_status = db.get_admins(user_id=call.from_user.id)[0]
    if user_status == "Admin":
        user = await bot.get_me()
        text = f"<b>🤖 {user.full_name} botining statistikasi.\n\n</b>"
        text += f"<i>👥 Botdagi foydalanuvchilar soni: {db.count_users()[0]}ta\n\n</i>"
        text += f"<i>👥 Obuna sotib olganlar soni: {len(db.select_users_subscription(subscription='True'))}\n\n</i>"
        text += f"<b><i>🔥 @{user.username} zo'r bot 💎</i></b>"
        await call.message.answer(text)
        await call.message.answer("<i><b>🧑‍💻 Siz admin panelidasiz. </b></i>", reply_markup=panel)
        await call.message.delete()
    else:
        await call.answer("🧑‍💻 Siz admin emassiz. ❌")

# Adminning ruhsatlarini o'zgartirish handlerlar jamlanmasi


@dp.callback_query_handler(text_contains="admin_rights:")
async def get_Admin_rights(call: types.CallbackQuery):
    id = call.data.replace("admin_rights:", "")
    user_datas = db.select_user_datas(user_id=id)
    text = f"👩🏻‍💻 <b>Admin:</b> <i><a href='tg://user?id={user_datas[1]}'>{user_datas[3]}</a></i>\n"
    text += "<i>uchun ruxsatlarni tanglang.</i>\n\n⚙️ O'zgartirish uchun o'sha ruxsatnomani ezing."
    await call.message.edit_text(text=text)
    await call.message.edit_reply_markup(reply_markup=change_admin_rights_2(admin_id=id))


@dp.callback_query_handler(text_contains="admin_change_admins:")
async def change_adminsdfsd_rights(call: types.CallbackQuery):
    id = call.data.replace("admin_change_admins:", "")
    rights = db.get_admin_rights(admin_id=id)
    if rights[2] == "Yes":
        db.update_admin_admin(
            admins="No",
            admin_id=id
        )
    else:
        db.update_admin_admin(
            admins="Yes",
            admin_id=id
        )
    await call.message.edit_reply_markup(reply_markup=change_admin_rights_2(admin_id=id))


@dp.callback_query_handler(text_contains="change_adminchanells:")
async def change_admidfgsdfgn_rights(call: types.CallbackQuery):
    id = call.data.replace("change_adminchanells:", "")
    rights = db.get_admin_rights(admin_id=id)
    if rights[3] == "Yes":
        db.update_admin_channels(
            channels="No",
            admin_id=id
        )
    else:
        db.update_admin_channels(
            channels="Yes",
            admin_id=id
        )
    await call.message.edit_reply_markup(reply_markup=change_admin_rights_2(admin_id=id))


@dp.callback_query_handler(text_contains="admin_change_ad:")
async def changsergserge_admin_rights(call: types.CallbackQuery):
    id = call.data.replace("admin_change_ad:", "")
    rights = db.get_admin_rights(admin_id=id)
    if rights[4] == "Yes":
        db.update_admin_send_post(
            send_post="No",
            admin_id=id
        )
    else:
        db.update_admin_send_post(
            send_post="Yes",
            admin_id=id
        )
    await call.message.edit_reply_markup(reply_markup=change_admin_rights_2(admin_id=id))


@dp.callback_query_handler(text_contains="admin_change_sendpost:")
async def change_athsrgsdfvxcvdmin_rights(call: types.CallbackQuery):
    id = call.data.replace("admin_change_sendpost:", "")
    rights = db.get_admin_rights(admin_id=id)
    if rights[5] == "Yes":
        db.update_admin_admin_post(
            admin_post="No",
            admin_id=id
        )
    else:
        db.update_admin_admin_post(
            admin_post="Yes",
            admin_id=id
        )
    await call.message.edit_reply_markup(reply_markup=change_admin_rights_2(admin_id=id))


@dp.callback_query_handler(text="zahiralarni_tahrirlash")
async def edit_test(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="USDT zahirasini kiriting:"
    )
    await ZahiraTahrirlash.usdt.set()


@dp.message_handler(state=ZahiraTahrirlash.usdt)
async def edit_usdt_backup(message: types.Message, state: FSMContext):
    await state.update_data({
        "usdt": message.text
    })
    await message.answer("So'm zahirasini kiriting: ")
    await ZahiraTahrirlash.next()


@dp.message_handler(state=ZahiraTahrirlash.som)
async def edit_som_backup(message: types.Message, state: FSMContext):
    try:
        datas = await state.get_data()
        db.update_zahira_som(
            som=f"{message.text}",
            id=1
        )
        db.update_zahira_usdt(
            usdt=datas['usdt'],
            id=1
        )
    except Exception as err:
        print(err)
    await state.finish()
    await message.answer("Muvaffaqiyatli o'zgartirildi.", reply_markup=panel)

# KURSLARNI tahrirlash


@dp.callback_query_handler(text="kurslarni_tahrirlash")
async def edit_test(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Olish kursni kiriting:"
    )
    await KursTahrirlash.olish.set()


@dp.message_handler(state=KursTahrirlash.olish)
async def edit_usdt_backup(message: types.Message, state: FSMContext):
    await state.update_data({
        "olish": message.text
    })
    await message.answer("Sotish kursini kiriting: ")
    await KursTahrirlash.next()


@dp.message_handler(state=KursTahrirlash.sotish)
async def edit_som_backup(message: types.Message, state: FSMContext):
    try:
        datas = await state.get_data()
        db.update_kurs_olish(
            olish=f"{datas['olish']}",
            id=1
        )
        db.update_kurs_sotish(
            sotish=f"{message.text}",
            id=1
        )
    except Exception as err:
        print(err)
    await state.finish()
    await message.answer("Muvaffaqiyatli o'zgartirildi.", reply_markup=panel)


@dp.message_handler(commands=['yangilash'])
async def check_subs_date(message: types.Message):
    if message.from_user.id == 1849953640:
        malumotlar = db.select_users_subscription(subscription="True")
        for data in malumotlar:
            date_str = f"{data[11]}"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
            today = datetime.today().date()
            if date_obj < today:
                text = "⚠️⏳ Sizning obunangiz muddati bugun tugadi,\npul ishlashda davom etay desangiz obunani yana qaytadan sotib oling."
                try:
                    await bot.send_message(chat_id=data[1], text=text, reply_markup=main_menu)
                except Exception as err:
                    pass
                try:
                    await db.update_user_subs(
                        subscription="False",
                        user_id=data[1]
                    )
                except Exception as err:
                    await bot.send_message(chat_id=DEVELOPER, text=f"{data[1]} - {data[3]} - foydalanuvchining obunasini o'chirishda xatolik ketdi! Obunani o'chirishda xatolik ketdi: {err}")
                    try:
                        await db.update_user_subs(
                            subscription="False",
                            user_id=data[1]
                        )
                    except:
                        pass
        await message.answer("Yangilandi ✅")
    else:
        await message.delete()
        await message.answer("Bu buyruq siz uchun emas ❌")


@dp.callback_query_handler(text="obunani_ochirish")
async def turn_off_subs(call: types.CallbackQuery):
    await BlockUserState.user_id.set()
    await call.message.edit_text(text="Obunasini o'chirmoqchi bo'lgan foydalanuvchining telegram_user_id sini kiriting: 👇", reply_markup=cancel_button)


@dp.message_handler(state=BlockUserState.user_id)
async def get_block_user_id(message: types.Message, state: FSMContext):
    message_text = message.text
    if db.check_user(user_id=message_text):
        await message.answer("Siz bergan id bo'yicha foydalanuvchi obunasi o'chirilmoqda! ✅")
        await bot.send_chat_action(chat_id=message.from_user.id, action=types.ChatActions.TYPING)
        await asyncio.sleep(2)
        try:
            db.update_user_subs(
                subscription="False",
                user_id=message_text
            )
            await state.finish()
            await message.answer("✅")
            await message.answer(
                text="Obuna holati muvaffaqiyatli o'chirildi! ✅",
                reply_markup=panel
            )
        except Exception as err:
            await message.answer("Xatolik ketdi va bu haqida dasturchi ogohlantirildi!\nMuammolar bo'lsa @Mistrdev ga murojaat qiling!", reply_markup=panel)
            await state.finish()
    else:
        await message.answer("Siz kiritgan ID bo'yicha foydalanuvchi topilmadi!\nQaytadan urinib ko'ring.")
