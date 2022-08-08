import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from utils.states import Form
from utils import database


async def add_channels(message: types.Message):
    await message.answer("Please write links of the channels you want to add")
    await Form.WAIT_MESSAGE.set()


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
    await Form.SETTINGS_MODE.set()


def register_settings_commands(dp: Dispatcher):
    dp.register_message_handler(add_channels, commands='add_channel', state=Form.SETTINGS_MODE)
    dp.register_message_handler(parse_and_add_channels, state=Form.WAIT_MESSAGE)
