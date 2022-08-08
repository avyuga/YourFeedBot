from aiogram import Dispatcher, types

from utils import database
from utils.keyboard import keyboard


async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    # todo: вынести подключение к БД
    database.find_user(user_id)
    await message.reply("Hi!\nI'm YourFeedBot! \nHere is the keyboard:",
                        reply_markup=keyboard)


async def send_help(message: types.Message):
    await message.reply("Hi!\nI'm YourFeedBot! \nHere is the keyboard:",
                        reply_markup=keyboard)


def register_basic_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start', state='*')
    dp.register_message_handler(send_help, commands='help', state='*')

