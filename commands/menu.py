from aiogram import Dispatcher, types

async def send_any_command_answer(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"You pressed the {callback.data} button")

def register_menu_commands(dp: Dispatcher):
    dp.register_callback_query_handler(send_any_command_answer,
                                       text=['add_channel', 'get_settings'],
                                       state='*')
