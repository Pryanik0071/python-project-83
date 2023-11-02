from flask import Flask, render_template


# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
