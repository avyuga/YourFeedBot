from aiogram import Dispatcher, types
from utils.keyboard import keyboard, menu_keyboard


async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    # todo: вынести подключение к БД
    # database.find_user(connection, cursor, user_id)
    await message.reply("Hi!\nI'm VuygaBot! \nHere is the keyboard:",
                        reply_markup=keyboard)

async def send_help(message: types.Message):
    await message.reply("Hi!\nI'm VuygaBot! \nHere is the keyboard:",
                        reply_markup=keyboard)

async def send_menu_from_command(message: types.Message):
    await message.reply("Here is the menu!", reply_markup=menu_keyboard)

async def send_menu_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Here is the menu!", reply_markup=menu_keyboard)


def register_basic_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start', state='*')
    dp.register_message_handler(send_help, commands='help', state='*')

    dp.register_message_handler(send_menu_from_command, commands='menu', state='*')
    dp.register_callback_query_handler(send_menu_from_button, text='menu', state='*')
