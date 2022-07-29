import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from utils.database import write_to_db, get_channels_list
from utils.states import Form


# async def add_channel_from_button(callback: types.CallbackQuery):
#     await callback.answer()
#     await callback.message.answer("please write the channels you want to add,"
#                                   " starting with @")
#     await Form.WAIT_MESSAGE.set()
    # await callback.message.answer(f"You pressed the ADD button")
    # await callback.message.answer('You are going to add channels here, but later')


# async def add_channel_from_command(message: types.Message):
#     await message.answer("please write the channels you want to add, "
#                          "starting with @")
#     await Form.WAIT_MESSAGE.set()


# async def parse_and_add_channels(message: types.Message, state: FSMContext):
#     channels = re.findall(r'@\w*\b', message.text)
#     logging.info(f"Channels: {channels}")
#     initial_list = get_channels_list(message.from_user.id)
#     number = 0
#     for channel in channels:
#         if channel not in initial_list:
#             write_to_db(message.from_user.id, channel)
#             number += 1
#         else:
#             logging.info(f"Channel {channel} is already in the list")
#     message_str = f"You have written {number} channels, others were already in!"
#     await message.answer(message_str)
#     await state.reset_state(with_data=False)
#     await Form.READY.set()


async def get_settings_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await Form.SETTINGS_MODE.set()
    await callback.message.answer(f"You entered the SETTINGS mode.")
    # todo add list of available commands
    await callback.message.answer('You can use this list of commands and buttons:')


async def get_settings_from_command(message: types.Message):
    await Form.SETTINGS_MODE.set()
    await message.answer("You entered the SETTINGS mode")


async def settings_mode():
    return

# попытка пересылки
# async def command_send_forward(message: types.Message):
#     # await bot.forward_message(, , message.message_id)
#     await message.answer("This section is not ready yet. \nPlease wait!")
# dp.register_message_handler(command_send_forward, commands='forward', state='*')

def register_menu_commands(dp: Dispatcher):
    # dp.register_callback_query_handler(add_channel_from_button,
    #                                    text='add_channel', state='*')
    # dp.register_message_handler(add_channel_from_command, commands='add_channel', state='*')
    # dp.register_message_handler(parse_and_add_channels, state=Form.WAIT_MESSAGE)

    dp.register_callback_query_handler(get_settings_from_button,
                                       text='get_settings', state='*')
    dp.register_message_handler(get_settings_from_command, commands='settings', state='*')
