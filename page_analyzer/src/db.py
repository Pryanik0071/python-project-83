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


def insert_new_url(name):
    conn = db_connect()
    with conn.cursor() as cur:
        query = "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id"
        cur.execute(query, (name, date.today()))
        id_ = cur.fetchone()[0]
        conn.commit()
    conn.close()
    return id_
