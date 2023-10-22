from aiogram.dispatcher.filters.state import StatesGroup, State


class DefaultState(StatesGroup):
    text = State()
    admin = State()
    post = State()
    adminss = State()


class AdminSendState(StatesGroup):
    photo = State()
    check = State()


class UserRegisterState(StatesGroup):
    fullname = State()
    phone = State()
    check = State()


class ConnectUs(StatesGroup):
    text = State()
    answer = State()

class SendResultState(StatesGroup):
    result = State()
    text = State()
    check = State()
    

class OperatorState(StatesGroup):
    user_id = State()
    answer = State()

class ChatgptState(StatesGroup):
    question = State()
    
    
class Test(StatesGroup):
  Test1 = State()
  Test2 = State()
  Test3 = State()
  Test4 = State()
  Test5 = State()
  Test6 = State()
  Test7 = State()
  Test8 = State()
  Test9 = State()
  Test10 = State()
