import os
from datetime import date

from dotenv import load_dotenv
from validators.url import url
import psycopg2
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, get_flashed_messages)


app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        name = request.form.get('url')
        if not url(name):
            flash('Некорректный URL', 'danger')
            return redirect(url_for('index'))
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"Select id from urls where name = \'{name}\'")
        url_id = cur.fetchone()
        if url_id is None:
            cur.execute(f"Insert into urls (name, created_at) "
                        f"VALUES ('{name}', '{date.today()}') RETURNING id")
            url_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_url', id=url_id))
        flash('Страница уже существует', 'info')
        url_id = url_id[0]
        return redirect(url_for('get_url', id=url_id))
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("Select id, name from urls ORDER BY id desc")
    urls_list = cur.fetchall()
    conn.close()
    return render_template('urls/index.html', urls=urls_list)


@app.route('/urls/<int:id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"Select name, created_at from urls where id= {id}")
    name, created_at = cur.fetchone()
    conn.close()
    return render_template('get_url/index.html',
                           messages=messages,
                           id=id,
                           name=name,
                           date=created_at)
