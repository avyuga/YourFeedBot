import logging
import re

from aiogram import Dispatcher, types

from utils.states import Form
from utils import database


# -------- ADD CHANNELS -------- #

async def add_channels_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await add_channels(callback.message)


async def add_channels(message: types.Message):
    await message.answer("Please write links of the channels you want to add")
    await Form.WAIT_MESSAGE_ADD.set()


async def parse_and_add_channels(message: types.Message):
    channels = []
    links = re.split(",", message.text)
    for link in links:
        items = re.split("/", link)
        channels += [items[-1]]
    logging.info(f"Channels: {channels}")
    initial_list = database.get_channels_list(message.from_user.id)
    number = 0
    for channel in channels:
        if channel not in initial_list:
            database.write_to_db(message.from_user.id, channel)
            number += 1
        else:
            logging.info(f"Channel {channel} is already in the list")
    message_str = f"You have written {number} channels, others were already in!"
    await message.answer(message_str)
    await Form.READY.set()


# -------- DELETE CHANNELS -------- #

async def delete_channels_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await delete_channels(callback.message)


async def delete_channels(message: types.Message):
    await message.answer("Please write links to channels you want to delete. "
                         "\nNOTE: channels you write should be in the list!")
    await Form.WAIT_MESSAGE_DELETE.set()


async def parse_and_delete_channels(message: types.Message):
    channels = []
    links = re.split(",", message.text)
    for link in links:
        items = re.split("/", link)
        channels += [items[-1]]
    logging.info(f"Channels: {channels}")
    # assume that channels to delete are in the list
    for channel in channels:
        database.delete_from_db(message.from_user.id, channel)
    message_str = f"You have deleted {len(channels)} channels, others are still in!"
    database.update_dates(message.from_user.id, length=len(channels))
    await message.answer(message_str)
    await Form.READY.set()


# --------- SHOW --------- #

async def show_list_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await show_list(callback.message, callback.from_user.id)


async def show_list(message: types.Message, user_id=0):
    if user_id == 0: user_id = message.from_user.id
    channels = database.get_channels_list(user_id)
    logging.info(channels)
    if len(channels) != 0:
        dates = database.get_last_message_dates(user_id)
        string = ''
        for (channel, date) in zip(channels, dates):
            string += f"\u2022 https://t.me/{channel} : {date}\n"
        await message.answer("Here are your channels and last messages received:\n" + string)
    else:
        await message.answer("No channels are written now.")


# --------- REGISTER --------- #

def register_settings_commands(dp: Dispatcher):
    # commands
    dp.register_message_handler(show_list, commands='show_channels', state=Form.READY)
    dp.register_message_handler(add_channels, commands='add_channel', state=Form.READY)
    dp.register_message_handler(delete_channels, commands='delete_channel', state=Form.READY)

    # parsers
    dp.register_message_handler(parse_and_add_channels, state=Form.WAIT_MESSAGE_ADD)
    dp.register_message_handler(parse_and_delete_channels, state=Form.WAIT_MESSAGE_DELETE)

    # buttons
    dp.register_callback_query_handler(show_list_from_button, text='show_channels', state=Form.READY)
    dp.register_callback_query_handler(add_channels_from_button, text='add_channel', state=Form.READY)
    dp.register_callback_query_handler(delete_channels_from_button, text='delete_channel', state=Form.READY)

