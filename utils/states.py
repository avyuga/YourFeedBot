from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    WAIT_MESSAGE_ADD = State()
    WAIT_MESSAGE_DELETE = State()
    READY = State()
    SETTINGS_MODE = State()