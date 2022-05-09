from aiogram import Dispatcher, types


async def add_channel_from_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"You pressed the ADD button")
    await callback.message.answer('You are going to add channels here, but later')


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

    dp.register_callback_query_handler(get_settings_from_button,
                                       text='get_settings', state='*')
    dp.register_message_handler(get_settings_from_command, commands='settings', state='*')


