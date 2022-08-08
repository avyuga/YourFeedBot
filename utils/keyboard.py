from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# todo добавить плашку help
button_menu = InlineKeyboardButton("Enter SETTINGS MODE", callback_data='settings')
keyboard = InlineKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_menu)

command_add = InlineKeyboardButton("Add channel", callback_data='add_channel')
command_delete = InlineKeyboardButton("Delete channel", callback_data='delete_channel')
command_quit_SM = InlineKeyboardButton("Quit SETTINGS MODE", callback_data='quit')
command_keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(command_add, command_delete, command_quit_SM)
