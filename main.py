import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboard import keyboard, menu_keyboard
from credentials import TOKEN

import database

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    WAIT_MESSAGE = State()
    READY = State()


user_id = ""


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    database.find_user(connection, cursor, user_id)
    await message.reply("Hi!\nI'm VuygaBot! \nHere is the keyboard:",
                        reply_markup=keyboard)


@dp.message_handler(commands=['help'], state=Form.READY)
async def send_help(message: types.Message):
    await message.reply("Hi!\nI'm VuygaBot! \nHere is the keyboard:",
                        reply_markup=keyboard)


# ----------KEYBOARD--------------------------#
@dp.callback_query_handler(lambda c: c.data == 'menu', state=Form.READY)
async def process_callback_make_menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,
                           "Here is the menu!",
                           reply_markup=menu_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'add_channel', state=Form.READY)
async def process_callback_add_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to add a channel. '
                                                        '\nPlease write channel names, starting from @, in a next '
                                                        'message.')
    await Form.WAIT_MESSAGE.set()


@dp.message_handler(state=Form.WAIT_MESSAGE)
async def parse_and_insert_channels(message: types.Message, state: FSMContext):
    channels = re.findall(r'@\w*\b', message.text)
    print(channels)
    await Form.READY.set()


@dp.callback_query_handler(lambda c: c.data == 'get_settings', state=Form.READY)
async def process_callback_show_settings(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to get settings')


# ----------COMMANDS---------------#
@dp.message_handler(commands=['menu'], state=Form.READY)
async def get_menu(message: types.Message):
    await message.reply("Here is the menu!", reply_markup=menu_keyboard)


@dp.message_handler(commands=['forward'], state=Form.READY)
async def send_forward(message: types.Message):
    # await bot.forward_message(, , message.message_id)
    await message.reply("if you see this, it's not forwarded yet")


@dp.message_handler(commands=['add_channel'], state=Form.READY)
async def add_channel(message: types.Message):
    await message.answer("This section is not ready yet. \nPlease wait!")


@dp.message_handler(state=Form.READY)
async def echo(message: types.Message):
    text = "Echo: " + message.text
    await message.answer(text)


if __name__ == '__main__':
    connection, cursor = database.initial_connect()
    if connection is None or cursor is None:
        exit(1)

    executor.start_polling(dp, skip_updates=True)

    database.close_connection(connection, cursor)
    exit(0)
