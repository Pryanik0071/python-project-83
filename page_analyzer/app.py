from .src import db, parser

import os

from dotenv import load_dotenv
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, get_flashed_messages)
from validators.url import url


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
        url_id = db.get_url_id(name)
        if url_id is not None:
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_url', id=url_id))
        url_id = db.insert_url(name)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=url_id))
    urls_list = db.get_urls()
    return render_template('urls/index.html', urls=urls_list)


@app.route('/urls/<int:id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url_info, url_checks = db.get_url_checks(id)
    return render_template('get_url/index.html', messages=messages,
                           url_info=url_info, url_checks=url_checks)


@app.post('/urls/<int:id>/checks')
def checks(id):
    url_ = db.get_url(id)
    result = parser.parse_url(url_)
    if result is None:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))
    flash('Страница успешно проверена', 'success')
    result['id'] = id
    db.insert_check(result)
    return redirect(url_for('get_url', id=id))
