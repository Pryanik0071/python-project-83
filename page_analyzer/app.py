from . import parser, db, validator

import os

from dotenv import load_dotenv
from flask import (Flask, render_template, request,
                   redirect, url_for, flash)


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        name = request.form.get('url')
        if not validator.is_valid(name):
            flash('Некорректный URL', 'alert-danger')
            return render_template('index.html'), 422
        normalize_name = validator.get_normalize_name(name)
        url_id = db.get_url_id(normalize_name)
        if url_id is not None:
            flash('Страница уже существует', 'alert-info')
            return redirect(url_for('get_url', id=url_id))
        url_id = db.insert_url(normalize_name)
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('get_url', id=url_id))
    urls_list = db.get_urls()
    return render_template('urls.html', urls=urls_list)


@app.route('/urls/<int:id>')
def get_url(id):
    url_info, url_checks = db.get_url_checks(id)
    return render_template('get_url.html',
                           url_info=url_info, url_checks=url_checks)


@app.post('/urls/<int:id>/checks')
def checks(id):
    name = db.get_url(id)
    result = parser.parse_url(name)
    if result is None:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_url', id=id))
    flash('Страница успешно проверена', 'alert-success')
    result['id'] = id
    db.insert_check(result)
    return redirect(url_for('get_url', id=id))
