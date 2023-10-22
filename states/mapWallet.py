from aiogram.dispatcher.filters.state import StatesGroup, State

class EditWallet(StatesGroup):
    EditUzcard = State()
    EditUzcardDate = State()
    EditHumo = State()
    EditHumoDate = State()
    EditQiwi = State()
    