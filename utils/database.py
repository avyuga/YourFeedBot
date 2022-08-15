import datetime

import psycopg2
import logging
from psycopg2 import Error
from psycopg2.extras import DictCursor

from credentials import DBNAME, USER, PASSWORD, HOST

logging.basicConfig(level=logging.INFO)

global connection
global cursor


def initial_connect():
    global connection, cursor
    try:
        connection = psycopg2.connect(dbname=DBNAME, user=USER,
                                      password=PASSWORD, host=HOST)
        connection.autocommit = True
        cursor = connection.cursor(cursor_factory=DictCursor)
    except (Exception, Error) as error:
        logging.error("Ошибка при инициализации PostgreSQL", error)
    finally:
        return connection, cursor

# {2022-05-20T18:11:48+00:00}


def find_user(user_id):
    global connection, cursor
    # user_id = 'test'
    cursor.execute(f"SELECT * FROM channels WHERE username = '{user_id}'")
    results = cursor.fetchall()
    if len(results) != 0:
        logging.warning(f"Пользователь {user_id} уже есть в базе данных.")
        # todo сделать кнопку - взять этот список или начать заново
        for row in results:
            print(f"{row['username']}: {row['list']}")
    else:
        cursor.execute(f"INSERT INTO channels VALUES('{user_id}', '{{}}', '{{}}')")


def get_user_ids():
    global connection, cursor
    query = """SELECT username FROM channels"""
    cursor.execute(query)
    result = cursor.fetchall()
    if cursor.rowcount == 0:
        return []
    return result[0]


def get_channels_list(user_id):
    global connection, cursor
    # query = """SELECT list FROM channels WHERE username = '%s' """
    cursor.execute(f"SELECT list FROM channels WHERE username = '{user_id}'")
    result = cursor.fetchall()
    # todo check indexing
    print(result[0][0])
    return result[0][0]


def get_last_message_dates(user_id):
    global connection, cursor
    # query = """SELECT dates FROM channels WHERE username = %s """
    cursor.execute(f"SELECT dates FROM channels WHERE username = '{user_id}'")
    result = cursor.fetchall()
    # todo check indexing
    return result[0][0]


def write_to_db(user_id, item):
    global connection, cursor
    # todo найти способ разом список заносить, при этом проверяя наличие
    # query = """ UPDATE channels SET list = array_append(list, %s)
    #             WHERE username = '%s' """
    cursor.execute(f' UPDATE channels SET list = array_append(list, \'{item}\') '
                   f'WHERE username = \'{user_id}\' ')
    # TODO заносить текущую дату при добавлении нового канала
    timing = datetime.datetime.now()
    timing_str = datetime.datetime.strftime(timing, f"%Y-%m-%dT%H:%M:%S+00:00")
    # 2022 - 05 - 20T18: 11:48 + 00: 00
    cursor.execute(f' UPDATE channels SET dates = array_append(dates, \'{timing_str}\') '
                   f'WHERE username = \'{user_id}\' ')


def delete_from_db(user_id, item):
    global connection, cursor
    cursor.execute(f' UPDATE channels SET list = array_remove(list, \'{item}\') '
                   f'WHERE username = \'{user_id}\' ')

    # initial_list = get_channels_list(user_id)
    # new_list = [item for item in initial_list if item not in items]
    #
    # timing = datetime.datetime.now()
    # timing_str = datetime.datetime.strftime(timing, f"%Y-%m-%dT%H:%M:%S+00:00")
    # new_dates = [timing_str for _ in range(len(new_list))]
    #
    # cursor.execute(f'UPDATE channels SET list = \'{new_list}\' WHERE username = \'{user_id}\' ')
    # cursor.execute(f'UPDATE channels SET dates = \'{new_dates}\' WHERE username = \'{user_id}\' ')


def update_dates(user_id, new_dates=None, length=0):
    global connection, cursor
    # query = """ UPDATE channels SET dates = %s WHERE username = '%s' """
    # cursor.execute(query, (new_dates, user_id)
    # cursor.execute(f" UPDATE channels SET dates =  '{{ \"{new_dates[0]}\" }}'"
    #                f" WHERE username = '{user_id}' ")
    if new_dates is not None:
        cursor.execute("UPDATE channels SET dates = %s WHERE username = %s", (new_dates, user_id))
    else:
        init_dates = get_last_message_dates(user_id)
        timing = datetime.datetime.now()
        timing_str = datetime.datetime.strftime(timing, f"%Y-%m-%dT%H:%M:%S+00:00")
        new_dates = [timing_str for _ in range(len(init_dates) - length)]
        cursor.execute("UPDATE channels SET dates = %s WHERE username = %s", (new_dates, str(user_id)))


def close_connection():
    global connection, cursor
    cursor.close()
    connection.close()
    logging.info("Соединение с PostgreSQL закрыто")
