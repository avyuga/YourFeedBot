
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --------- COMMANDS KEYBOARD --------- #
command_show = InlineKeyboardButton("Show channels", callback_data='show_channels')
command_add = InlineKeyboardButton("Add channel", callback_data='add_channel')
command_delete = InlineKeyboardButton("Delete channel", callback_data='delete_channel')
command_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)\
    .add(command_show, command_add, command_delete)


get_commands_button = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(
    "List of commands", callback_data='get_commands'))

quit_button = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(
    "Quit", callback_data='quit'))