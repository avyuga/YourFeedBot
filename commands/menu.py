import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from utils.database import write_to_db
from utils.states import Form


async def add_channel_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("please write the channels you want to add,"
                                  " starting with @")
    await Form.WAIT_MESSAGE.set()
    # await callback.message.answer(f"You pressed the ADD button")
    # await callback.message.answer('You are going to add channels here, but later')


async def parsing_channels(message: types.Message, state: FSMContext):
    channels = re.findall(r'@\w*\b', message.text)
    logging.info(f"Channels: {channels}")
    write_to_db(message.from_user.id, channels[0])
    message_str = "You have written channels:"
    for i in range(len(channels)):
        message_str += (" " + channels[i] + ",")
    message_str += " that's all!"
    await message.answer(message_str)
    await state.reset_state(with_data=False)
    await Form.READY.set()


async def add_channel_from_command(message: types.Message):
    await message.answer("This section is not ready yet. \nPlease wait!")


async def get_settings_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"You pressed the SETTINGS button")
    await callback.message.answer('You are going to get settings list, but later')

async def get_settings_from_command(message: types.Message):
    await message.answer("This section is not ready yet. \nPlease wait!")

# попытка пересылки
# async def command_send_forward(message: types.Message):
#     # await bot.forward_message(, , message.message_id)
#     await message.answer("This section is not ready yet. \nPlease wait!")
# dp.register_message_handler(command_send_forward, commands='forward', state='*')

def register_menu_commands(dp: Dispatcher):
    dp.register_callback_query_handler(add_channel_from_button,
                                       text='add_channel', state='*')
    dp.register_message_handler(add_channel_from_command, commands='add_channel', state='*')
    dp.register_message_handler(parsing_channels, state=Form.WAIT_MESSAGE)

    dp.register_callback_query_handler(get_settings_from_button,
                                       text='get_settings', state='*')
    dp.register_message_handler(get_settings_from_command, commands='settings', state='*')


