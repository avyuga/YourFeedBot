from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    READY = State()
    WAIT_MESSAGE_ADD = State()
    WAIT_MESSAGE_DELETE = State()
