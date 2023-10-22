from aiogram.dispatcher.filters.state import State, StatesGroup


class BlockUserState(StatesGroup):
    user_id = State()

    