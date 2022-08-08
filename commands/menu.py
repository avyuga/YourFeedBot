from aiogram import Dispatcher, types
from utils.states import Form
from utils.keyboard import command_keyboard


async def get_settings_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await settings_mode(callback.message)


async def get_settings_from_command(message: types.Message):
    await settings_mode(message)


async def settings_mode(message: types.Message):
    await Form.SETTINGS_MODE.set()
    await message.answer("You entered the SETTINGS MODE. "
                         "\nYou can use this list of commands and buttons:",
                         reply_markup=command_keyboard)


# попытка пересылки
# async def command_send_forward(message: types.Message):
#     # await bot.forward_message(, , message.message_id)
#     await message.answer("This section is not ready yet. \nPlease wait!")
# dp.register_message_handler(command_send_forward, commands='forward', state='*')

async def quit_settings_mode(callback: types.CallbackQuery):
    await callback.answer()
    await Form.READY.set()
    await callback.message.answer("You have quit the SETTINGS MODE.")


def register_menu_commands(dp: Dispatcher):
    # dp.register_callback_query_handler(add_channel_from_button,
    #                                    text='add_channel', state='*')
    # dp.register_message_handler(add_channel_from_command, commands='add_channel', state='*')
    # dp.register_message_handler(parse_and_add_channels, state=Form.WAIT_MESSAGE)

    dp.register_callback_query_handler(get_settings_from_button,
                                       text='settings', state='*')
    dp.register_message_handler(get_settings_from_command, commands='settings', state='*')

    dp.register_callback_query_handler(quit_settings_mode, text='quit', state='*')
