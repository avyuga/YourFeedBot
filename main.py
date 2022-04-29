import logging

from aiogram import Bot, Dispatcher, executor, types

from keyboard import keyboard, menu_keyboard
from credentials import TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm VuygaBot! \nHere is the keyboard:",
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'add_channel')
async def process_callback_add_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to add a channel')


@dp.callback_query_handler(lambda c: c.data == 'get_settings')
async def process_callback_add_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, 'You are going to get settings')


@dp.callback_query_handler(lambda c: c.data == 'menu')
async def process_callback_add_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,
                           "Here is the menu!",
                           reply_markup=menu_keyboard)

@dp.message_handler(commands=['menu'])
async def get_menu(message: types.Message):
    await message.reply("Here is the menu!", reply_markup=menu_keyboard)

@dp.message_handler(commands=['forward'])
async def send_forward(message: types.Message):
    # await bot.forward_message(, , message.message_id)
    await message.reply("if you see this, it's not forwarded yet")


@dp.message_handler(commands=['add_channel'])
async def add_channel(message: types.Message):
    await message.answer("This section is not ready yet. \nPlease wait!")


@dp.message_handler()
async def echo(message: types.Message):
    text = "Echo: " + message.text
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
