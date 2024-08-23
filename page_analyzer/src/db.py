from datetime import date
import os

import psycopg2
from psycopg2.extras import DictCursor


DATABASE_URL = os.getenv('DATABASE_URL')


def db_connect():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    conn = db_connect()
    with conn.cursor() as cur:
        query = """SELECT id, name,
        last_check.status_code as status_code,
        last_check.created_at as created
        FROM urls LEFT JOIN (
            SELECT DISTINCT ON (url_id)
            url_id, status_code, created_at
            FROM url_checks
            ORDER by url_id, created_at DESC) as last_check
        ON last_check.url_id = id
        ORDER BY id DESC;"""
        cur.execute(query)
        urls_list = cur.fetchall()
    conn.close()
    return urls_list


def get_url_id(url):
    conn = db_connect()
    with conn.cursor() as cur:
        query = "SELECT id FROM urls WHERE name = %s"
        cur.execute(query, (url,))
        id_ = cur.fetchone()
    conn.close()
    if id_:  # If is not None
        return id_[0]
    return id_


def insert_url(name):
    conn = db_connect()
    with conn.cursor() as cur:
        query = """INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id"""
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


def get_url_checks(url_id):
    result = []
    conn = db_connect()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        query = """SELECT
                urls.id as url_id,
                name,
                urls.created_at as url_created,
                url_checks.id as id,
                url_checks.status_code as status_code,
                url_checks.h1 as h1,
                url_checks.title as title,
                url_checks.description as description,
                url_checks.created_at as created
            FROM urls
            LEFT JOIN url_checks
            ON urls.id = url_checks.url_id
            WHERE urls.id = %s
            ORDER BY url_checks.id DESC;"""
        cur.execute(query, (url_id,))
        data = cur.fetchall()
        for check in data:
            result.append({
                'url_id': check['url_id'],
                'name': check['name'],
                'id': check['id'],
                'url_created': check['url_created'],
                'status_code': check['status_code'],
                'h1': check['h1'],
                'title': check['title'],
                'description': check['description'],
                'created': check['created']
            })
    conn.close()
    url_info = {
        'url_id': result[0]['url_id'],
        'name': result[0]['name'],
        'url_created': result[0]['url_created'],
    }
    return url_info, result
