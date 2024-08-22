from datetime import date
import os

import psycopg2


DATABASE_URL = os.getenv('DATABASE_URL')


def db_connect():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    conn = db_connect()
    with conn.cursor() as cur:
        query = "SELECT id, name FROM urls ORDER BY id DESC"
        cur.execute(query)
        urls_list = cur.fetchall()
    conn.close()
    return urls_list


def check_url_in_db(name):
    conn = db_connect()
    with conn.cursor() as cur:
        query = "SELECT id FROM urls WHERE name = %s"
        cur.execute(query, (name,))
        id_ = cur.fetchone()
    conn.close()
    if id_:  # If is not None
        return id_[0]
    return id_


def insert_url(name):
    conn = db_connect()
    with conn.cursor() as cur:
        query = "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id"
        cur.execute(query, (name, date.today()))
        id_ = cur.fetchone()[0]
        conn.commit()
    conn.close()
    return id_


def get_url(url_id):
    conn = db_connect()
    with conn.cursor() as cur:
        query = "SELECT name FROM urls WHERE id = %s"
        cur.execute(query, (url_id,))
        name = cur.fetchone()[0]
    conn.close()
    return name


def insert_check(data):
    conn = db_connect()
    with conn.cursor() as cur:
        query = """
            INSERT INTO url_checks 
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%(id)s, %(code)s, %(h1)s, %(title)s, %(desc)s, %(date)s)
            """
        cur.execute(query, data)
        conn.commit()
    conn.close()



# SELECT
#     id,
# 	name,
# 	last_check.status_code,
# 	last_check.created_at
# 	from urls
# 	left join (
#         SELECT DISTINCT ON (url_id)
#         url_id,
# 	    status_code,
# 	    created_at
# 		FROM url_checks
# 		ORDER by url_id, created_at DESC) as last_check
#     on last_check.url_id = id;