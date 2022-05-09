import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand

from commands import basic, menu
from utils import database
from credentials import TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
# todo прикрутить столбец в БД
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    WAIT_MESSAGE = State()
    READY = State()


user_id = ""

basic.register_basic_commands(dp)
menu.register_menu_commands(dp)

# ----------KEYBOARD--------------------------#

@dp.callback_query_handler(lambda c: c.data == 'add_channel')
async def process_callback_add_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to add a channel. '
                                                        '\nPlease write channel names, starting from @, in a next '
                                                        'message.')
    await Form.WAIT_MESSAGE.set()


async def parse_channels(message: types.Message, state: FSMContext):
    channels = re.findall(r'@\w*\b', message.text)
    print("Channels ", channels)
    user_data = await state.get_data()
    print("User_data: ", user_data)
    await message.answer("First channel is: ", channels[0])
    await state.reset_state(with_data=False)

# @dp.message_handler(state=Form.WAIT_MESSAGE)
# async def parse_and_insert_channels(message: types.Message, state: FSMContext):
#     channels = re.findall(r'@\w*\b', message.text)
#     print(channels)
#     await Form.READY.set()


@dp.callback_query_handler(lambda c: c.data == 'get_settings')
async def process_callback_show_settings(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to get settings')


# ----------COMMANDS---------------#

@dp.message_handler(commands=['forward'])
async def send_forward(message: types.Message):
    # await bot.forward_message(, , message.message_id)
    await message.reply("if you see this, it's not forwarded yet")


@dp.message_handler(commands=['add_channel'])
async def add_channel(message: types.Message):
    await message.answer("This section is not ready yet. \nPlease wait!")


@dp.message_handler()
async def echo(message: types.Message):
    text = "Echo: " + message.text
    await message.answer(text)

#
# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(command="/start", description="Start"),
#         BotCommand(command="/menu", description="Call for starting menu"),
#         BotCommand(command="/add", description="Add a channel"),
#         BotCommand(command="/settings", description="Go to settings")
#     ]
#     await bot.set_my_commands(commands)


if __name__ == '__main__':
    connection, cursor = database.initial_connect()
    if connection is None or cursor is None:
        exit(1)

    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/menu", description="Call for starting menu"),
        BotCommand(command="/add", description="Add a channel"),
        BotCommand(command="/settings", description="Go to settings")
    ]
    # bot.set_my_commands(commands)

    executor.start_polling(dp, skip_updates=True)

    database.close_connection(connection, cursor)
    exit(0)
