from aiogram.dispatcher.filters.state import State, StatesGroup

class ZahiraTahrirlash(StatesGroup):
    usdt = State()
    som = State()
    

class KursTahrirlash(StatesGroup):
    olish = State()
    sotish = State()