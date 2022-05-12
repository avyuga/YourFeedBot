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

def find_user(user_id):
    global connection, cursor
    # user_id = 'test'
    cursor.execute(f"SELECT * FROM channels WHERE username = '{user_id}'")
    results = cursor.fetchall()
    if len(results) != 0:
        logging.warning(f"Пользователь {user_id} уже есть в базе данных.")
        # todo сделать кнопочку - взять этот список или начать заново
        for row in results:
            print(f"{row['username']}: {row['list']}")
    else:
        cursor.execute(f"INSERT INTO channels VALUES('{user_id}', '{{}}')")


def get_channels_list(user_id):
    global connection, cursor
    query = """ SELECT list FROM channels WHERE username = '%s' """
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    return result[0][0]

def write_to_db(user_id, item):
    global connection, cursor
    # todo найти способ разом список заносить, при этом проверяя наличие
    query = """ UPDATE channels SET list = array_append(list, %s) 
                WHERE username = '%s' """
    cursor.execute(query, (item, user_id))


def close_connection():
    global connection, cursor
    cursor.close()
    connection.close()
    logging.info("Соединение с PostgreSQL закрыто")
