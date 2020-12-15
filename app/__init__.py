from __future__ import unicode_literals

import logging
from logging.handlers import RotatingFileHandler
import os
import sqlite3

from werkzeug.utils import secure_filename
from flask import (
    g,
    Flask,
    jsonify,
    send_from_directory,
    render_template,
    request,
    redirect,
    url_for
)

import youtube_dl

HISTORY_TABLE = '''
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY,
    title TEXT,
    webpage_url TEXT UNIQUE)
'''

def create_app():
    app = Flask(__name__)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/xstreamly.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('xstreamly startup')

    return app


app = create_app()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database')
        db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(HISTORY_TABLE)
    db.commit()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    stream_url = request.form['url'] if request.method == 'POST' else request.args.get('url')
    
    if stream_url:
        result = {}
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(stream_url, download=False)
            save_history(result['title'], result['webpage_url'])
        
        return render_template('index.html', stream=result, history=load_history())
    return render_template('index.html', history=load_history())


def load_history():
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('''SELECT title, webpage_url FROM history ORDER BY id DESC''')
        result = cursor.fetchall()
        # print(f'load_history: {result}')
        cursor.close()
        return result


def save_history(title, webpage_url):
    if not title or not webpage_url:
        return

    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('''INSERT OR IGNORE INTO history(title, webpage_url)
                  VALUES(?,?)''', (title, webpage_url))
        get_db().commit()
        # print(f'save_history({title}, {webpage_url})')
        