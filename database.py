import psycopg2
import logging
from psycopg2 import Error
from credentials import DBNAME, USER, PASSWORD, HOST


logging.basicConfig(level=logging.INFO)

def initial_connect():
    connection = None
    cursor = None
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

def find_user(connection, cursor, user_id):
    # user_id = 'test'
    cursor.execute(f"SELECT * FROM channels WHERE username = '{user_id}'")
    results = cursor.fetchall()
    if len(results) != 0:
        logging.warning(f"Пользователь {user_id} уже есть в базе данных.")
        # todo сделать кнопочку - взять этот список или начать заново
        for row in results:
            print(row)
    else:
        cursor.execute(f"INSERT INTO channels VALUES('{user_id}', '{{blah}}')")
        connection.commit()

def close_connection(connection, cursor):
    cursor.close()
    connection.close()
    logging.info("Соединение с PostgreSQL закрыто")
