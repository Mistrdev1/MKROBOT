import aioschedule
import asyncio
from loader import bot, db
import functools
import datetime

async def send_function():
    vaqt = datetime.datetime.now()
    keyingivaqt = vaqt.strftime("%H:%M")
    malumotlar = db.select_posts_times(send_time=keyingivaqt)
    for malumot in malumotlar:
        for guruh in db.select_groups():
            await bot.send_photo(chat_id=guruh[1],photo=malumot[1], caption=malumot[2])
        send_clock = datetime.timedelta(minutes=int(malumot[3]))
        dt = datetime.datetime.strptime(malumot[4], "%H:%M")
        # dt_str = dt.strftime("%H:%M")
        finish_time = dt + send_clock
        finally_time = finish_time.strftime("%H:%M")
        db.update_send_time(
            send_time=finally_time,
            id=malumot[0]
        )

async def daily_tasks():
    job_func = functools.partial(send_function)
    vaqt = datetime.datetime.now()
    send_clock = datetime.timedelta(minutes=1)
    finish_time = vaqt + send_clock
    finally_time = finish_time.strftime("%H:%M")
    db.update_all_times(
        send_time=finally_time
    )
    aioschedule.every(23).seconds.do(job_func)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
    
                