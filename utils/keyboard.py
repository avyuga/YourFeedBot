from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_start = InlineKeyboardButton("Add", callback_data='add_channel')
button_settings = InlineKeyboardButton("Settings", callback_data='get_settings')
menu_keyboard = InlineKeyboardMarkup().add(button_start, button_settings)

button_menu = InlineKeyboardButton("Menu", callback_data='menu')
keyboard = InlineKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_menu)
