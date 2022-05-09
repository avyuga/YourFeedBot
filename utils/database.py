import psycopg2
import logging
from psycopg2 import Error
from credentials import DBNAME, USER, PASSWORD, HOST


logging.basicConfig(level=logging.INFO)

global connection
global cursor

def initial_connect():
    global connection, cursor
    try:
        connection = psycopg2.connect(dbname=DBNAME, user=USER,
                                      password=PASSWORD, host=HOST)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM channels")
        for row in cursor:
            print(row)
    except (Exception, Error) as error:
        logging.error("Ошибка при инициализации PostgreSQL", error)
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
            print(row)
    else:
        cursor.execute(f"INSERT INTO channels VALUES('{user_id}', '{{}}')")
        connection.commit()

def write_to_db(user_id, item):
    global connection, cursor
    # todo найти способ разом список заносить
    query = """ UPDATE channels SET list = array_append(list, %s) 
                WHERE username = '%s' """
    cursor.execute(query, (item, user_id))
    connection.commit()

def close_connection():
    global connection, cursor
    cursor.close()
    connection.close()
    logging.info("Соединение с PostgreSQL закрыто")
