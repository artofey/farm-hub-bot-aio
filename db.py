import os
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import closing

DATABASE_URL = os.environ.get('DATABASE_URL')


def sql_request_to_db(SQL, *args):
    try:
        with closing(psycopg2.connect(DATABASE_URL)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                conn.autocommit = True
                cursor.execute(SQL, args)
                if args is ():
                    result = cursor.fetchall()
                    return result
    except psycopg2.Error as err:
        print("Query error: {}".format(err))


def get_defers_list_from_db():
    result = sql_request_to_db('SELECT * FROM defers_list')
    list = []
    for item in result:
        list.append(item[0])
    return list


def add_defer_to_db(defer_name):
    sql_request_to_db('INSERT INTO defers_list (name) VALUES (%s)', defer_name)


def del_defer_from_db(defer_name):
    sql_request_to_db('DELETE FROM defers_list * WHERE name=%s', defer_name)


def del_all_defers_from_db():
    sql_request_to_db('DELETE FROM defers_list *')


def create_table_defers_list():
    sql_request_to_db('''CREATE TABLE
                         defers_list (name VARCHAR(64) PRIMARY KEY)''')
