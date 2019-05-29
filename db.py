# import os
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import closing

DATABASE_URL = 'postgres://test:test@localhost:5432/yarovenkoay'


def sql_request_to_db(SQL, *args):
    with closing(psycopg2.connect(DATABASE_URL)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(SQL, *args)
            result = cursor.fetchall()
    return result


def get_defers_list_from_db():
    result = []
    
    pass


def add_defer_to_db(defer_name):
    sql_request_to_db('INSERT INTO defers_list (name) VALUES (%s)', defer_name)


def del_defer_from_db(defer_name):
    sql_request_to_db('DELETE FROM defers_list * WHERE name=%s', defer_name)


print(get_defers_list_from_db())
