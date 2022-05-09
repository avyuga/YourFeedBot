from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    WAIT_MESSAGE = State()
    READY = State()