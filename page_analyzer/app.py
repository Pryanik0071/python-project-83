import os
from datetime import date

from dotenv import load_dotenv
from validators.url import url
import psycopg2
import requests
from .src import db
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, get_flashed_messages)


app = Flask(__name__)

load_dotenv()
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
        url_id = db.check_url_in_db(name)
        if url_id is not None:
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_url', id=url_id))
        url_id = db.insert_new_url(name)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=url_id))
    urls_list = db.get_urls()
    return render_template('urls/index.html', urls=urls_list)


@app.route('/urls/<int:id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    conn = db.db_connect()
    with conn.cursor() as cur:
        query = "SELECT name, created_at FROM urls WHERE id=%s"
        cur.execute(query, (id,))
        name, created_at = cur.fetchone()
        cur.execute(f"Select id, status_code, h1, title, description, created_at from url_checks where url_id = {id} ORDER BY id desc ")
        all_checks = cur.fetchall()
    conn.close()
    return render_template('get_url/index.html',
                           messages=messages,
                           id=id,
                           name=name,
                           date=created_at,
                           checks=all_checks)


@app.post('/urls/<int:id>/checks')
def checks(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"Select name from urls where id= {id}")
    name = cur.fetchone()[0]
    r = requests.get(name)
    status_code = r.status_code
    cur.execute(f"Insert into url_checks (url_id, created_at) "
                f"VALUES ('{id}', '{date.today()}')")
    conn.commit()
    conn.close()
    return redirect(url_for('get_url', id=id))


# TODO:
# Внешний вид подсматривайте здесь
# Учитесь пользоваться логами, они ваш главный помощник
# Для нормализации имени сайта используйте urlparse
# Для валидации имени сайта используйте validators
# Для заполнения created_at используйте datetime
# Для работы с переменными окружения используйте python-dotenv

# Реализуйте валидацию для введенного URL-адреса. У URL обязательно должен быть валидный адрес, не превышающий 255 символов
# Реализуйте вывод конкретного введенного URL на отдельной странице urls/<id>
# Реализуйте вывод всех добавленных URL на отдельной странице /urls и проверьте, что новые записи отображаются первыми
# Задеплойте результат