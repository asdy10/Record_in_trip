from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    date = State()
    trip = State()
    count = State()
    count_need_more = State()
    phone = State()
    name = State()
    confirm = State()

