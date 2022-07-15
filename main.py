import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from commands import basic, menu
from utils import database
from credentials import TOKEN
from updates.parser import check_updates
import aioschedule, asyncio
# Configure logging
# fixme починить логгирование
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
# todo прикрутить столбец в БД
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

basic.register_basic_commands(dp)
menu.register_menu_commands(dp)

@dp.message_handler()
async def echo(message: types.Message):
    text = "Echo: " + message.text
    await message.answer(text)


# todo Здесь прописать рассылку для каждого пользователя
async def job(user_id):
    channels = database.get_channels_list(user_id)
    for channel in channels:
        last_message = None
        check_updates(channel, last_message)
        # check_updates
        print(channel)
    await bot.send_message(int(user_id), "JOB DONE")


async def scheduler():
    # для каждого user'а запускать свой job
    # наладить время обновления, 5 секунд - слишком коротко
    users = database.get_user_ids()
    for user in users:
        aioschedule.every(5).seconds.do(job, user_id=user)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())

# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(command="/start", description="Start"),
#         BotCommand(command="/menu", description="Call for starting menu"),
#         BotCommand(command="/add", description="Add a channel"),
#         BotCommand(command="/settings", description="Go to settings")
#     ]
#     await bot.set_my_commands(commands)


if __name__ == '__main__':
    connection, cursor = database.initial_connect()
    if connection is None or cursor is None:
        exit(1)

    # commands = [
    #     BotCommand(command="/start", description="Start"),
    #     BotCommand(command="/menu", description="Call for starting menu"),
    #     BotCommand(command="/add", description="Add a channel"),
    #     BotCommand(command="/settings", description="Go to settings")
    # ]
    # bot.set_my_commands(commands)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    database.close_connection()
    exit(0)
