from aiogram import Dispatcher, types

from utils import database
from utils.states import Form

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --------- KEYBOARD --------- #
# todo добавить плашку help

command_show = InlineKeyboardButton("Show channels", callback_data='show_channels')
command_add = InlineKeyboardButton("Add channel", callback_data='add_channel')
command_delete = InlineKeyboardButton("Delete channel", callback_data='delete_channel')
command_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)\
    .add(command_show, command_add, command_delete)

button = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(
    "List of commands", callback_data='get_commands'))


# ---------- START & HELP ---------- #

async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    # todo: вынести подключение к БД
    database.find_user(user_id)
    await message.reply("Hi! I'm YourFeedBot!")


async def send_help(message: types.Message):
    await message.reply("To get list of commands, type /get_commands or press the button\u2193", reply_markup=button)


# ---------- COMMANDS UTILS --------- #
# TODO make analogically in SETTINGS_MODE
async def get_commands_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await get_commands(callback.message)


async def get_commands(message: types.Message):
    await Form.READY.set()
    await message.answer("You can use this list of commands:\n"
                         "\u2022 /start - start the Bot, \n"
                         "\u2022 /help - help with commands, \n"
                         "\u2022 /show_channels - show the list of channels, \n"
                         "\u2022 /add_channel - add channel to the list, \n"
                         "\u2022 /delete_channel - delete channel from the list\n"
                         "Here are the buttons for some \u2193",
                         reply_markup=command_keyboard)


# попытка пересылки
# async def command_send_forward(message: types.Message):
#     # await bot.forward_message(, , message.message_id)
#     await message.answer("This section is not ready yet. \nPlease wait!")
# dp.register_message_handler(command_send_forward, commands='forward', state='*')


def register_menu_commands(dp: Dispatcher):
    # start & help commands
    dp.register_message_handler(send_welcome, commands='start', state='*')
    dp.register_message_handler(send_help, commands='help', state='*')

    dp.register_callback_query_handler(get_commands_from_button, text='get_commands', state='*')
    dp.register_message_handler(get_commands, commands='get_commands', state='*')
