import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from commands import menu, settings_mode
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

menu.register_menu_commands(dp)
settings_mode.register_settings_commands(dp)


@dp.message_handler()
async def echo(message: types.Message):
    text = "Echo: " + message.text
    await message.answer(text)


# todo Здесь прописать рассылку для каждого пользователя
# todo def send user's feed
async def job():
    users = database.get_user_ids()
    logging.warning(users)
    for user_id in users:
        channels = database.get_channels_list(user_id)
        message_dates = database.get_last_message_dates(user_id)
        new_dates = []
        for i in range(len(channels)):
            channel = channels[i]
            last_message = message_dates[i]
            last_message = datetime.datetime.strptime(last_message, f"%Y-%m-%dT%H:%M:%S+{last_message[-5:]}")
            res, new_date = check_updates(channel, last_message)
            new_dates += [new_date]
            # check_updates
            print(res)
            if res != '':
                await bot.send_message(int(user_id), res, parse_mode='markdown')
        if len(channels) != 0: database.update_dates(user_id, new_dates)


# todo записать цикл в job, там же организовать получение нового списка
async def scheduler():
    aioschedule.every(10).seconds.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
    # # для каждого user'а запускать свой job
    # # наладить время обновления, 5 секунд - слишком коротко
    # users = database.get_user_ids()
    # logging.warning(users)
    # for user in users:
    #     res = aioschedule.every(10).seconds.do(job, user_id=user)
    #     logging.warning(res)
    # while True:
    #     await aioschedule.run_pending()
    #     await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    connection, cursor = database.initial_connect()
    if connection is None or cursor is None:
        exit(1)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    database.close_connection()
    exit(0)
